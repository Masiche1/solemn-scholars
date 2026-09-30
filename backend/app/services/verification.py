"""Private verification storage, malware scanning, and retention operations."""
import os
import secrets
import shutil
import subprocess
from datetime import datetime, timedelta

from flask import current_app
from werkzeug.utils import secure_filename

from app import db
from app.models import VerificationDocument, VerificationSubmission


class VerificationUploadError(ValueError):
    """Raised when a verification upload cannot be safely accepted."""


_ALLOWED_TYPES = {
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
    ".png": ("image/png", b"\x89PNG\r\n\x1a\n"),
    ".pdf": ("application/pdf", b"%PDF"),
}


def store_verification_upload(upload, document_type, user_id):
    """Validate, scan, and store one upload in the private verification volume."""
    if not upload or not upload.filename:
        return None

    original = secure_filename(upload.filename)
    extension = os.path.splitext(original)[1].lower()
    if not original or extension not in _ALLOWED_TYPES:
        raise VerificationUploadError("Use JPG, PNG, or PDF files.")
    if document_type == "selfie" and extension == ".pdf":
        raise VerificationUploadError("Selfies must be JPG or PNG files.")

    upload.stream.seek(0, os.SEEK_END)
    size = upload.stream.tell()
    upload.stream.seek(0)
    max_bytes = current_app.config["VERIFICATION_MAX_FILE_BYTES"]
    if size <= 0 or size > max_bytes:
        raise VerificationUploadError(
            f"Each file must be between 1 byte and {max_bytes // (1024 * 1024)} MB."
        )

    header = upload.stream.read(8)
    upload.stream.seek(0)
    mime_type, signature = _ALLOWED_TYPES[extension]
    if not header.startswith(signature):
        raise VerificationUploadError(f"{original} does not match its file type.")

    storage_key = f"{user_id}/{secrets.token_urlsafe(32)}{extension}"
    root = current_app.config["VERIFICATION_UPLOAD_DIR"]
    destination = os.path.join(root, storage_key.replace("/", os.sep))
    os.makedirs(os.path.dirname(destination), mode=0o700, exist_ok=True)
    upload.save(destination)
    try:
        _scan_or_reject(destination)
    except VerificationUploadError:
        _remove_file(destination)
        raise
    return storage_key, original, mime_type, size


def _scan_or_reject(path):
    """Run the configured scanner; fail closed when production scanning is required."""
    command = current_app.config.get("VERIFICATION_SCAN_COMMAND", "clamdscan")
    required = current_app.config["VERIFICATION_REQUIRE_SCAN"]
    executable = shutil.which(command)
    if not executable:
        if required:
            raise VerificationUploadError("Uploads are temporarily unavailable because malware scanning is not configured.")
        return
    try:
        result = subprocess.run(
            [executable, "--no-summary", path],
            capture_output=True,
            text=True,
            timeout=current_app.config["VERIFICATION_SCAN_TIMEOUT_SECONDS"],
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        if required:
            raise VerificationUploadError("The malware scanner did not respond. Please try again later.") from exc
        return
    if result.returncode != 0:
        raise VerificationUploadError("This file did not pass malware scanning and was rejected.")


def _remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def purge_verification_data(now=None):
    """Delete files and records past the configured retention period."""
    now = now or datetime.utcnow()
    policies = (
        ("rejected", current_app.config["VERIFICATION_REJECTED_RETENTION_DAYS"]),
        ("approved", current_app.config["VERIFICATION_APPROVED_RETENTION_DAYS"]),
    )
    deleted_documents = 0
    deleted_submissions = 0
    for status, days in policies:
        cutoff = now - timedelta(days=days)
        documents = VerificationDocument.query.join(VerificationSubmission).filter(
            VerificationSubmission.status == status,
            VerificationDocument.uploaded_at < cutoff,
        ).all()
        for document in documents:
            path = os.path.join(current_app.config["VERIFICATION_UPLOAD_DIR"], document.storage_key.replace("/", os.sep))
            _remove_file(path)
            document.deleted_at = now
            db.session.delete(document)
            deleted_documents += 1

        submissions = VerificationSubmission.query.filter(
            VerificationSubmission.status == status,
            VerificationSubmission.submitted_at < cutoff,
        ).all()
        for submission in submissions:
            db.session.delete(submission)
            deleted_submissions += 1

    db.session.commit()
    return deleted_submissions, deleted_documents

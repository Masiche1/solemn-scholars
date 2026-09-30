"""Tutor authenticated area."""
import secrets
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app, session
from flask_login import current_user, login_required
from app import db
from app.models import (TutorProfile, Subject, Availability, Application, Job,
                        Conversation, Message, User, Booking, Review, VerificationSubmission, VerificationDocument)
from app.services.helpers import tutor_required, get_or_404, slugify
from app.services.verification import store_verification_upload, VerificationUploadError
from datetime import datetime, timedelta

tutor_bp = Blueprint("tutor", __name__)


@tutor_bp.route("/dashboard")
@login_required
@tutor_required
def dashboard():
    profile = current_user.tutor_profile
    if not profile:
        profile = TutorProfile(user_id=current_user.id, profile_status="draft", verification_status="unverified")
        db.session.add(profile)
        db.session.commit()
    applications = Application.query.filter_by(tutor_id=current_user.id).order_by(Application.created_at.desc()).limit(5).all()
    convo_count = _my_conversations().count()
    upcoming = Booking.query.filter(
        Booking.tutor_id == current_user.id, Booking.start_at >= datetime.utcnow(),
        Booking.status.in_(["pending", "confirmed"])
    ).order_by(Booking.start_at.asc()).limit(5).all()
    return render_template("tutor/dashboard.html", profile=profile, applications=applications,
                           convo_count=convo_count, upcoming=upcoming)


@tutor_bp.route("/profile", methods=["GET", "POST"])
@login_required
@tutor_required
def edit_profile():
    profile = current_user.tutor_profile
    if not profile:
        profile = TutorProfile(user_id=current_user.id, profile_status="draft", verification_status="unverified")
        db.session.add(profile)
        db.session.commit()
    all_subjects = Subject.query.order_by(Subject.name).all()
    if request.method == "POST":
        action = request.form.get("action", "save")
        profile.headline = request.form.get("headline", "").strip()
        profile.biography = request.form.get("biography", "").strip()
        profile.teaching_approach = request.form.get("teaching_approach", "").strip()
        profile.qualifications = request.form.get("qualifications", "").strip()
        profile.years_experience = request.form.get("years_experience", type=int) or 0
        profile.hourly_rate = request.form.get("hourly_rate", type=float) or profile.hourly_rate
        profile.teaching_modes = ",".join(request.form.getlist("teaching_modes")) or "online"
        profile.location_name = request.form.get("location_name", "").strip()
        profile.languages = request.form.get("languages", "").strip()
        profile.response_time = request.form.get("response_time", "within a few hours").strip()

        # subjects
        selected = request.form.getlist("subjects")
        profile.subjects = Subject.query.filter(Subject.slug.in_(selected)).all()

        # availability: rebuild
        Availability.query.filter_by(tutor_id=profile.id).delete()
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for wd in weekdays:
            enabled = request.form.get(f"avail_{wd}") == "1"
            if enabled:
                start = request.form.get(f"avail_{wd}_start", "17:00")
                end = request.form.get(f"avail_{wd}_end", "20:00")
                db.session.add(Availability(tutor_id=profile.id, weekday=wd, start_time=start,
                                             end_time=end, timezone="Europe/London", recurring=True))

        if action == "submit":
            profile.profile_status = "pending"
            flash("Your profile has been submitted for review. Our team will approve it shortly.", "success")
        else:
            flash("Profile saved.", "success")
        db.session.commit()
        return redirect(url_for("tutor.edit_profile"))
    return render_template("tutor/edit_profile.html", profile=profile, all_subjects=all_subjects)


@tutor_bp.route("/job-feed")
@login_required
@tutor_required
def job_feed():
    profile = current_user.tutor_profile
    if not profile or profile.profile_status != "approved":
        flash("Complete and submit your profile to access the job feed.", "info")
        return redirect(url_for("tutor.edit_profile"))
    jobs = Job.query.filter_by(status="open").order_by(Job.created_at.desc()).all()
    applied_ids = {a.job_id for a in Application.query.filter_by(tutor_id=current_user.id).all()}
    return render_template("tutor/job_feed.html", jobs=jobs, applied_ids=applied_ids, profile=profile)


@tutor_bp.route("/applications")
@login_required
@tutor_required
def applications():
    apps = Application.query.filter_by(tutor_id=current_user.id).order_by(Application.created_at.desc()).all()
    return render_template("tutor/applications.html", applications=apps)


@tutor_bp.route("/messages")
@login_required
@tutor_required
def messages():
    conversations = _my_conversations().all()
    return render_template("tutor/messages.html", conversations=conversations, active_convo=None)


@tutor_bp.route("/messages/<int:convo_id>", methods=["GET", "POST"])
@login_required
@tutor_required
def message_thread(convo_id):
    convo = get_or_404(Conversation, convo_id)
    if current_user.id not in (convo.participant_a_id, convo.participant_b_id):
        abort(403)
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            other_id = convo.other_participant(current_user.id)
            db.session.add(Message(conversation_id=convo.id, sender_id=current_user.id,
                                   recipient_id=other_id, body=body))
            for m in convo.messages:
                if m.recipient_id == current_user.id and not m.read_at:
                    m.read_at = datetime.utcnow()
            db.session.commit()
            flash("Message sent.", "success")
            return redirect(url_for("tutor.message_thread", convo_id=convo_id))
    for m in convo.messages:
        if m.recipient_id == current_user.id and not m.read_at:
            m.read_at = datetime.utcnow()
    db.session.commit()
    other = User.query.get(convo.other_participant(current_user.id))
    conversations = _my_conversations().all()
    return render_template("tutor/messages.html", conversations=conversations,
                           active_convo=convo, other_user=other)


@tutor_bp.route("/calendar")
@login_required
@tutor_required
def calendar():
    profile = current_user.tutor_profile
    availability = profile.availability if profile else []
    bookings = Booking.query.filter_by(tutor_id=current_user.id).order_by(Booking.start_at.asc()).all()
    return render_template("tutor/calendar.html", availability=availability, bookings=bookings)


@tutor_bp.route("/bookings/<int:booking_id>/<string:action>", methods=["POST"])
@login_required
@tutor_required
def booking_action(booking_id, action):
    booking = get_or_404(Booking, booking_id)
    if booking.tutor_id != current_user.id:
        abort(403)
    if action == "confirm":
        booking.status = "confirmed"
        flash("Booking confirmed. It will now show on the student's dashboard.", "success")
    elif action == "cancel":
        booking.status = "cancelled"
        flash("Booking cancelled.", "info")
    elif action == "complete":
        booking.status = "completed"
        booking.payment_status = "paid"
        flash("Booking marked as completed. The student can now leave a review.", "success")
    else:
        abort(404)
    db.session.commit()
    return redirect(url_for("tutor.calendar"))


@tutor_bp.route("/earnings")
@login_required
@tutor_required
def earnings():
    bookings = Booking.query.filter_by(tutor_id=current_user.id).all()
    completed = [b for b in bookings if b.status == "completed"]
    total = sum(b.price for b in completed)
    commission_rate = 0.15
    commission = total * commission_rate
    net = total - commission
    return render_template("tutor/earnings.html", completed=completed, total=total,
                           commission=commission, net=net)


@tutor_bp.route("/reviews")
@login_required
@tutor_required
def reviews():
    profile = current_user.tutor_profile
    reviews = profile.reviews_received if profile else []
    return render_template("tutor/reviews.html", reviews=reviews, profile=profile)


@tutor_bp.route("/verification", methods=["GET", "POST"])
@login_required
@tutor_required
def verification():
    profile = current_user.tutor_profile
    if not profile:
        profile = TutorProfile(user_id=current_user.id, profile_status="draft", verification_status="unverified")
        db.session.add(profile)
        db.session.commit()
    if request.method == "POST":
        if not secrets.compare_digest(request.form.get("csrf_token", ""), session.get("csrf_token", "")):
            abort(400, description="Invalid CSRF token.")
        if request.form.get("documents_confirmed") != "1":
            flash("Confirm that the submitted documents are genuine before continuing.", "error")
            return redirect(url_for("tutor.verification"))
        if profile.verification_status == "pending":
            flash("Your verification is already under review.", "info")
            return redirect(url_for("tutor.verification"))

        uploads = {key: request.files.get(key) for key in ("id_doc", "qual_doc", "background_doc", "selfie_doc")}
        if any(not uploads[key] or not uploads[key].filename for key in ("id_doc", "qual_doc")):
            flash("Government-issued ID and qualification proof are required.", "error")
            return redirect(url_for("tutor.verification"))

        staged = []
        try:
            for field_name, upload in uploads.items():
                if not upload or not upload.filename:
                    continue
                stored = store_verification_upload(upload, field_name.replace("_doc", ""), current_user.id)
                staged.append((field_name.replace("_doc", ""), *stored))
        except VerificationUploadError as exc:
            for _, storage_key, *_ in staged:
                try:
                    from app.services.verification import _remove_file
                    _remove_file(os.path.join(current_app.config["VERIFICATION_UPLOAD_DIR"], storage_key.replace("/", os.sep)))
                except OSError:
                    pass
            flash(str(exc), "error")
            return redirect(url_for("tutor.verification"))

        submission = VerificationSubmission(tutor_id=profile.id, status="pending")
        db.session.add(submission)
        for document_type, storage_key, original, mime_type, size in staged:
            submission.documents.append(VerificationDocument(document_type=document_type, storage_key=storage_key,
                                                              original_filename=original, mime_type=mime_type, file_size=size))
        profile.verification_status = "pending"
        db.session.commit()
        flash("Your verification documents have been submitted for review.", "success")
        return redirect(url_for("tutor.verification"))
    latest = profile.verification_submissions[0] if profile.verification_submissions else None
    return render_template("tutor/verification.html", profile=profile,
                           verification_documents=latest.documents if latest else [],
                           verification_rejection_reason=latest.rejection_reason if latest else None)


@tutor_bp.route("/settings", methods=["GET", "POST"])
@login_required
@tutor_required
def settings():
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name)
        current_user.phone = request.form.get("phone", current_user.phone)
        new_pw = request.form.get("new_password", "").strip()
        if new_pw:
            if len(new_pw) < 6:
                flash("New password must be at least 6 characters.", "error")
            else:
                current_user.set_password(new_pw)
                flash("Password updated.", "success")
        db.session.commit()
        flash("Account settings saved.", "success")
        return redirect(url_for("tutor.settings"))
    return render_template("tutor/settings.html")


def _my_conversations():
    return Conversation.query.filter(
        db.or_(Conversation.participant_a_id == current_user.id,
               Conversation.participant_b_id == current_user.id)
    ).order_by(Conversation.created_at.desc())

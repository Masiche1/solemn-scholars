"""Admin area: moderation, user management, leads, analytics."""
import os
import secrets
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app, send_file, session
from flask_login import current_user, login_required
from app import db
from app.models import (User, TutorProfile, Job, Application, Lead, Review, Booking,
                        VerificationSubmission, VerificationDocument, VerificationAccessLog)
from app.services.helpers import admin_required, get_or_404
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
@admin_required
def overview():
    stats = {
        "users": User.query.count(),
        "tutors": TutorProfile.query.count(),
        "approved_tutors": TutorProfile.query.filter_by(profile_status="approved").count(),
        "pending_profiles": TutorProfile.query.filter_by(profile_status="pending").count(),
        "jobs": Job.query.count(),
        "open_jobs": Job.query.filter_by(status="open").count(),
        "applications": Application.query.count(),
        "leads": Lead.query.count(),
        "new_leads": Lead.query.filter_by(lifecycle_status="new").count(),
        "bookings": Booking.query.count(),
        "completed_bookings": Booking.query.filter_by(status="completed").count(),
        "reviews": Review.query.count(),
        "flagged_reviews": Review.query.filter_by(moderation_status="flagged").count(),
    }
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
    pending_profiles = TutorProfile.query.filter_by(profile_status="pending").limit(5).all()
    return render_template("admin/overview.html", stats=stats, recent_leads=recent_leads,
                           pending_profiles=pending_profiles)


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    q = request.args.get("q", "").strip()
    role = request.args.get("role", "").strip()
    query = User.query
    if q:
        query = query.filter(db.or_(User.name.ilike(f"%{q}%"), User.email.ilike(f"%{q}%")))
    if role:
        query = query.filter_by(role=role)
    users = query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users, q=q, role=role)


@admin_bp.route("/users/<int:user_id>/status", methods=["POST"])
@login_required
@admin_required
def user_status(user_id):
    user = get_or_404(User, user_id)
    new_status = request.form.get("status")
    if new_status in ("active", "suspended", "pending"):
        user.status = new_status
        db.session.commit()
        flash(f"User {user.name} marked as {new_status}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/tutor-approvals")
@login_required
@admin_required
def tutor_approvals():
    pending = TutorProfile.query.filter(db.or_(TutorProfile.profile_status.in_(["pending", "draft"]),
                                               TutorProfile.verification_status == "pending")).all()
    verification_queue = VerificationSubmission.query.filter_by(status="pending").order_by(
        VerificationSubmission.submitted_at.asc()).all()
    return render_template("admin/tutor_approvals.html", pending=pending, verification_queue=verification_queue)


@admin_bp.route("/verification/<int:submission_id>/<string:action>", methods=["POST"])
@login_required
@admin_required
def review_verification(submission_id, action):
    submission = get_or_404(VerificationSubmission, submission_id)
    if not secrets.compare_digest(request.form.get("csrf_token", ""), session.get("csrf_token", "")):
        abort(400, description="Invalid CSRF token.")
    if submission.status != "pending" or action not in ("approve", "reject"):
        abort(400, description="This verification submission is no longer reviewable.")
    reason = request.form.get("rejection_reason", "").strip()
    if action == "reject" and not reason:
        flash("A rejection reason is required.", "error")
        return redirect(url_for("admin.tutor_approvals"))
    submission.status = "approved" if action == "approve" else "rejected"
    submission.reviewed_at = datetime.utcnow()
    submission.reviewed_by = current_user.id
    submission.rejection_reason = reason or None
    submission.tutor_profile.verification_status = "verified" if action == "approve" else "rejected"
    for document in submission.documents:
        document.status = "approved" if action == "approve" else "rejected"
        document.rejection_reason = reason or None
        document.reviewed_at = datetime.utcnow()
    db.session.commit()
    flash("Verification approved." if action == "approve" else "Verification rejected.", "success")
    return redirect(url_for("admin.tutor_approvals"))


@admin_bp.route("/verification/documents/<int:document_id>")
@login_required
@admin_required
def verification_document(document_id):
    document = get_or_404(VerificationDocument, document_id)
    path = os.path.join(current_app.config["VERIFICATION_UPLOAD_DIR"], document.storage_key.replace("/", os.sep))
    if document.deleted_at or not os.path.isfile(path):
        abort(404)
    db.session.add(VerificationAccessLog(document_id=document.id, admin_id=current_user.id, action="download"))
    db.session.commit()
    return send_file(path, mimetype=document.mime_type, as_attachment=True,
                     download_name=document.original_filename)


@admin_bp.route("/tutor-approvals/<int:profile_id>", methods=["POST"])
@login_required
@admin_required
def approve_profile(profile_id):
    profile = get_or_404(TutorProfile, profile_id)
    action = request.form.get("action")
    if action == "approve":
        profile.profile_status = "approved"
        flash(f"Profile for {profile.user.name} approved.", "success")
    elif action == "reject":
        profile.profile_status = "rejected"
        flash(f"Profile for {profile.user.name} rejected.", "info")
    elif action == "verify":
        profile.verification_status = "verified"
        flash(f"{profile.user.name} verified.", "success")
    elif action == "unverify":
        profile.verification_status = "unverified"
        flash(f"Verification removed for {profile.user.name}.", "info")
    db.session.commit()
    return redirect(url_for("admin.tutor_approvals"))


@admin_bp.route("/job-moderation")
@login_required
@admin_required
def job_moderation():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template("admin/job_moderation.html", jobs=jobs)


@admin_bp.route("/job-moderation/<int:job_id>", methods=["POST"])
@login_required
@admin_required
def moderate_job(job_id):
    job = get_or_404(Job, job_id)
    action = request.form.get("action")
    if action == "close":
        job.status = "closed"
        flash("Job closed.", "success")
    elif action == "reopen":
        job.status = "open"
        flash("Job reopened.", "success")
    elif action == "moderate":
        job.status = "moderated"
        flash("Job removed from feed pending review.", "info")
    db.session.commit()
    return redirect(url_for("admin.job_moderation"))


@admin_bp.route("/leads")
@login_required
@admin_required
def leads():
    status = request.args.get("status", "").strip()
    query = Lead.query
    if status:
        query = query.filter_by(lifecycle_status=status)
    leads = query.order_by(Lead.created_at.desc()).all()
    return render_template("admin/leads.html", leads=leads, status=status)


@admin_bp.route("/leads/<int:lead_id>", methods=["POST"])
@login_required
@admin_required
def update_lead(lead_id):
    lead = get_or_404(Lead, lead_id)
    new_status = request.form.get("lifecycle_status")
    if new_status in ("new", "contacted", "matched", "converted", "lost"):
        lead.lifecycle_status = new_status
        if request.form.get("assigned_to"):
            lead.assigned_to = request.form.get("assigned_to")
        db.session.commit()
        flash(f"Lead #{lead.id} updated to {new_status}.", "success")
    return redirect(url_for("admin.leads"))


@admin_bp.route("/reviews")
@login_required
@admin_required
def reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template("admin/reviews.html", reviews=reviews)


@admin_bp.route("/reviews/<int:review_id>", methods=["POST"])
@login_required
@admin_required
def moderate_review(review_id):
    review = get_or_404(Review, review_id)
    action = request.form.get("action")
    if action == "approve":
        review.moderation_status = "approved"
    elif action == "flag":
        review.moderation_status = "flagged"
    elif action == "remove":
        review.moderation_status = "removed"
    db.session.commit()
    flash(f"Review #{review.id} moderation updated.", "success")
    return redirect(url_for("admin.reviews"))


@admin_bp.route("/analytics")
@login_required
@admin_required
def analytics():
    # Conversion funnel-style metrics
    total_leads = Lead.query.count()
    converted = Lead.query.filter_by(lifecycle_status="converted").count()
    matched = Lead.query.filter_by(lifecycle_status="matched").count()
    total_bookings = Booking.query.count()
    completed = Booking.query.filter_by(status="completed").count()
    revenue = sum(b.price for b in Booking.query.filter_by(status="completed").all())
    commission = revenue * 0.15

    # signups over last 14 days (simple)
    cutoff = datetime.utcnow() - timedelta(days=14)
    recent_users = User.query.filter(User.created_at >= cutoff).count()

    # subject distribution
    from app.models import Subject, tutor_subjects
    subject_counts = db.session.query(Subject.name, db.func.count(tutor_subjects.c.tutor_profile_id)).join(
        tutor_subjects, tutor_subjects.c.subject_id == Subject.id
    ).group_by(Subject.id).order_by(db.desc(db.func.count(tutor_subjects.c.tutor_profile_id))).all()

    return render_template("admin/analytics.html", total_leads=total_leads, converted=converted,
                           matched=matched, total_bookings=total_bookings, completed=completed,
                           revenue=revenue, commission=commission, recent_users=recent_users,
                           subject_counts=subject_counts)

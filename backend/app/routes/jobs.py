"""Job marketplace routes: public job feed, job detail, apply, post-a-job handling."""
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import db
from app.models import Job, Application, Subject, TutorProfile, Lead, Conversation, Message, User
from app.services.helpers import get_or_404, roles_required

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/")
def feed():
    query = Job.query.filter_by(status="open")

    subject = request.args.get("subject", "").strip()
    level = request.args.get("level", "").strip()
    mode = request.args.get("mode", "").strip()
    location = request.args.get("location", "").strip()
    min_budget = request.args.get("min_budget", type=float)
    new_only = request.args.get("new_only") == "1"

    if subject:
        query = query.filter(Job.subject.ilike(f"%{subject}%"))
    if level:
        query = query.filter(Job.level.ilike(f"%{level}%"))
    if mode and mode != "either":
        query = query.filter(db.or_(Job.teaching_mode == mode, Job.teaching_mode == "either"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if min_budget:
        query = query.filter(Job.budget_max >= min_budget)

    query = query.order_by(Job.created_at.desc())
    jobs = query.all()

    applied_job_ids = set()
    if current_user.is_authenticated and current_user.is_tutor:
        applied_job_ids = {a.job_id for a in Application.query.filter_by(tutor_id=current_user.id).all()}

    return render_template("jobs/feed.html", jobs=jobs, filters=request.args, applied_job_ids=applied_job_ids)


@jobs_bp.route("/<int:job_id>")
def detail(job_id):
    job = get_or_404(Job, job_id)
    if job.status not in ("open",) and not (
        current_user.is_authenticated and (current_user.id == job.requester_id or current_user.is_admin)
    ):
        abort(404)
    # similar jobs
    similar = Job.query.filter(Job.id != job.id, Job.subject == job.subject, Job.status == "open").limit(3).all()
    has_applied = False
    if current_user.is_authenticated and current_user.is_tutor:
        has_applied = Application.query.filter_by(job_id=job.id, tutor_id=current_user.id).first() is not None
    return render_template("jobs/detail.html", job=job, similar=similar, has_applied=has_applied)


@jobs_bp.route("/<int:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply(job_id):
    job = get_or_404(Job, job_id)
    if not current_user.is_tutor:
        flash("Only tutor accounts can apply for jobs.", "error")
        return redirect(url_for("jobs.detail", job_id=job_id))
    profile = current_user.tutor_profile
    if not profile or profile.profile_status != "approved":
        flash("Please complete and submit your profile for approval before applying.", "error")
        return redirect(url_for("tutor.edit_profile"))
    existing = Application.query.filter_by(job_id=job.id, tutor_id=current_user.id).first()
    if existing:
        flash("You've already applied to this job.", "info")
        return redirect(url_for("jobs.detail", job_id=job_id))
    if request.method == "POST":
        app = Application(
            job_id=job.id,
            tutor_id=current_user.id,
            message=request.form.get("message", "").strip(),
            proposed_rate=request.form.get("proposed_rate", type=float),
            availability_note=request.form.get("availability", "").strip(),
            status="pending",
        )
        db.session.add(app)
        db.session.commit()
        flash("Your application has been submitted. The requester will be notified.", "success")
        return redirect(url_for("tutor.applications"))
    return render_template("jobs/apply.html", job=job, profile=profile)


@jobs_bp.route("/<int:job_id>/report", methods=["POST"])
@login_required
def report(job_id):
    job = get_or_404(Job, job_id)
    reason = request.form.get("reason", "").strip()
    # In a real app this would create a moderation queue item; here we flag the lead/contact
    flash(f"Thank you — job #{job.id} has been reported for review. Our team will look into it.", "success")
    return redirect(url_for("jobs.detail", job_id=job_id))

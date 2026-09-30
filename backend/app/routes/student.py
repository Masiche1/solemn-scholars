"""Student/parent authenticated area."""
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import db
from app.models import (SavedTutor, TutorProfile, Conversation, Message, Job, Booking,
                        Review, User, Application)
from app.services.helpers import student_required, get_or_404
from datetime import datetime

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
@login_required
@student_required
def dashboard():
    saved_count = len(current_user.saved_tutors)
    my_jobs = Job.query.filter_by(requester_id=current_user.id).order_by(Job.created_at.desc()).all()
    my_bookings = Booking.query.filter_by(learner_id=current_user.id).order_by(Booking.created_at.desc()).limit(5).all()
    convo_count = _my_conversations().count()
    return render_template("student/dashboard.html", saved_count=saved_count, my_jobs=my_jobs,
                           my_bookings=my_bookings, convo_count=convo_count)


@student_bp.route("/saved")
@login_required
@student_required
def saved_tutors():
    saved = current_user.saved_tutors
    return render_template("student/saved_tutors.html", saved=saved)


@student_bp.route("/messages")
@login_required
@student_required
def messages():
    return _render_messages()


@student_bp.route("/messages/<int:convo_id>", methods=["GET", "POST"])
@login_required
@student_required
def message_thread(convo_id):
    convo = get_or_404(Conversation, convo_id)
    if current_user.id not in (convo.participant_a_id, convo.participant_b_id):
        abort(403)
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            other_id = convo.other_participant(current_user.id)
            msg = Message(conversation_id=convo.id, sender_id=current_user.id,
                          recipient_id=other_id, body=body)
            db.session.add(msg)
            # mark thread read
            for m in convo.messages:
                if m.recipient_id == current_user.id and not m.read_at:
                    m.read_at = datetime.utcnow()
            db.session.commit()
            flash("Message sent.", "success")
            return redirect(url_for("student.message_thread", convo_id=convo_id))
    for m in convo.messages:
        if m.recipient_id == current_user.id and not m.read_at:
            m.read_at = datetime.utcnow()
    db.session.commit()
    other = User.query.get(convo.other_participant(current_user.id))
    conversations = _my_conversations().all()
    return render_template("student/messages.html", conversations=conversations,
                           active_convo=convo, other_user=other)


@student_bp.route("/job-requests", methods=["GET", "POST"])
@login_required
@student_required
def job_requests():
    if request.method == "POST":
        job = Job(
            requester_id=current_user.id,
            title=request.form.get("title", "").strip(),
            subject=request.form.get("subject", "").strip(),
            level=request.form.get("level", "").strip(),
            goals=request.form.get("goals", "").strip(),
            teaching_mode=request.form.get("teaching_mode", "online"),
            location=request.form.get("location", "").strip(),
            budget_min=request.form.get("budget_min", type=float),
            budget_max=request.form.get("budget_max", type=float),
            schedule=request.form.get("schedule", "").strip(),
            start_date=request.form.get("start_date", "").strip(),
            additional_details=request.form.get("details", "").strip(),
            status="open",
            expires_at=datetime.utcnow().replace(hour=23, minute=59) + __import__("datetime").timedelta(days=30),
        )
        if not job.title or not job.subject:
            flash("Please provide at least a title and subject.", "error")
            return redirect(url_for("student.job_requests"))
        db.session.add(job)
        db.session.commit()
        flash("Your tutoring request is now live on the job feed.", "success")
        return redirect(url_for("student.job_requests"))
    my_jobs = Job.query.filter_by(requester_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template("student/job_requests.html", my_jobs=my_jobs)


@student_bp.route("/job-requests/<int:job_id>/applicants")
@login_required
@student_required
def job_applicants(job_id):
    job = get_or_404(Job, job_id)
    if job.requester_id != current_user.id:
        abort(403)
    applications = Application.query.filter_by(job_id=job.id).order_by(Application.created_at.desc()).all()
    return render_template("student/job_applicants.html", job=job, applications=applications)


@student_bp.route("/job-requests/<int:job_id>/applicants/<int:app_id>/<string:action>", methods=["POST"])
@login_required
@student_required
def job_applicant_action(job_id, app_id, action):
    job = get_or_404(Job, job_id)
    if job.requester_id != current_user.id:
        abort(403)
    application = get_or_404(Application, app_id)
    if application.job_id != job.id:
        abort(404)
    if action == "accept":
        application.status = "accepted"
        # decline other pending applications for this job automatically
        for other in Application.query.filter_by(job_id=job.id).all():
            if other.id != application.id and other.status == "pending":
                other.status = "declined"
        job.status = "closed"
        db.session.commit()
        flash(f"You accepted {application.tutor_user.name}'s application. Other applicants were notified.", "success")
        # start a conversation between requester and tutor so they can arrange the lesson
        _get_or_create_conversation(current_user.id, application.tutor_id)
        db.session.commit()
    elif action == "decline":
        application.status = "declined"
        db.session.commit()
        flash(f"You declined {application.tutor_user.name}'s application.", "info")
    else:
        abort(404)
    return redirect(url_for("student.job_applicants", job_id=job.id))


def _get_or_create_conversation(a_id, b_id):
    convo = Conversation.query.filter(
        db.or_(
            db.and_(Conversation.participant_a_id == a_id, Conversation.participant_b_id == b_id),
            db.and_(Conversation.participant_a_id == b_id, Conversation.participant_b_id == a_id),
        )
    ).first()
    if not convo:
        convo = Conversation(participant_a_id=a_id, participant_b_id=b_id)
        db.session.add(convo)
        db.session.flush()
    return convo


@student_bp.route("/bookings")
@login_required
@student_required
def bookings():
    my_bookings = Booking.query.filter_by(learner_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("student/bookings.html", bookings=my_bookings)


@student_bp.route("/reviews")
@login_required
@student_required
def reviews():
    my_reviews = Review.query.filter_by(author_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template("student/reviews.html", reviews=my_reviews)


@student_bp.route("/bookings/<int:booking_id>/review", methods=["GET", "POST"])
@login_required
@student_required
def leave_review(booking_id):
    booking = get_or_404(Booking, booking_id)
    if booking.learner_id != current_user.id:
        abort(403)
    if booking.status != "completed":
        flash("You can only review a session after it's completed.", "error")
        return redirect(url_for("student.bookings"))
    if booking.review:
        flash("You've already reviewed this session.", "info")
        return redirect(url_for("student.bookings"))
    tutor_profile = TutorProfile.query.filter_by(user_id=booking.tutor_id).first()
    if request.method == "POST":
        rating = request.form.get("rating", type=int) or 5
        rating = max(1, min(5, rating))
        comment = request.form.get("comment", "").strip()
        review = Review(
            booking_id=booking.id,
            author_id=current_user.id,
            recipient_id=tutor_profile.id,
            rating=rating,
            comment=comment,
            moderation_status="approved",
        )
        db.session.add(review)
        db.session.commit()
        flash("Thanks! Your review has been posted.", "success")
        return redirect(url_for("student.bookings"))
    return render_template("student/leave_review.html", booking=booking, tutor_profile=tutor_profile)


@student_bp.route("/settings", methods=["GET", "POST"])
@login_required
@student_required
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
        return redirect(url_for("student.settings"))
    return render_template("student/settings.html")


def _my_conversations():
    return Conversation.query.filter(
        db.or_(Conversation.participant_a_id == current_user.id,
               Conversation.participant_b_id == current_user.id)
    ).order_by(Conversation.created_at.desc())


def _render_messages():
    conversations = _my_conversations().all()
    return render_template("student/messages.html", conversations=conversations, active_convo=None)

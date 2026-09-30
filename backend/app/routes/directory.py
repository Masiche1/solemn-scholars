"""Tutor directory and profile pages."""
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import db
from app.models import TutorProfile, Subject, SavedTutor, Conversation, Message, User, Booking
from app.services.helpers import get_or_404, roles_required
from datetime import datetime

directory_bp = Blueprint("directory", __name__)


@directory_bp.route("/")
def directory():
    query = TutorProfile.query.filter_by(profile_status="approved")

    # Filters
    subject = request.args.get("subject", "").strip()
    level = request.args.get("level", "").strip()
    location = request.args.get("location", "").strip()
    mode = request.args.get("mode", "").strip()
    q = request.args.get("q", "").strip()
    min_rating = request.args.get("min_rating", type=float)
    max_price = request.args.get("max_price", type=float)
    verified_only = request.args.get("verified") == "1"
    sort = request.args.get("sort", "recommended")

    if subject:
        subj = Subject.query.filter_by(slug=subject).first()
        if subj:
            query = query.filter(TutorProfile.subjects.contains(subj))
    if location:
        query = query.filter(TutorProfile.location_name.ilike(f"%{location}%"))
    if mode == "online":
        query = query.filter(TutorProfile.teaching_modes.ilike("%online%"))
    elif mode == "in-person":
        query = query.filter(TutorProfile.teaching_modes.ilike("%in-person%"))
    if verified_only:
        query = query.filter_by(verification_status="verified")
    if max_price:
        query = query.filter(TutorProfile.hourly_rate <= max_price)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(TutorProfile.headline.ilike(like), TutorProfile.biography.ilike(like))
        )

    # Sort (DB-level for real columns; Python-level for computed properties like avg_rating)
    if sort == "lowest-price":
        query = query.order_by(TutorProfile.hourly_rate.asc())
    elif sort == "most-experienced":
        query = query.order_by(TutorProfile.years_experience.desc())
    elif sort == "recently-joined":
        query = query.order_by(TutorProfile.created_at.desc())
    elif sort == "highest-rated":
        query = query.order_by(TutorProfile.completed_lessons.desc())  # base order before Python re-sort
    else:  # recommended
        query = query.order_by(TutorProfile.completed_lessons.desc())

    tutors = query.all()

    if sort == "highest-rated":
        # avg_rating is a computed Python property, not a DB column, so sort in Python.
        # Tutors with no reviews (avg_rating is None) fall to the end.
        tutors = sorted(tutors, key=lambda t: (t.avg_rating is None, -(t.avg_rating or 0)))

    # post-filter by rating (computed property)
    if min_rating:
        tutors = [t for t in tutors if t.avg_rating >= min_rating]

    subjects = Subject.query.order_by(Subject.name).all()
    saved_ids = set()
    if current_user.is_authenticated and current_user.is_student:
        saved_ids = {s.tutor_profile_id for s in current_user.saved_tutors}

    return render_template("directory/directory.html", tutors=tutors, subjects=subjects,
                           filters=request.args, saved_ids=saved_ids)


@directory_bp.route("/<int:tutor_id>")
def tutor_profile(tutor_id):
    profile = get_or_404(TutorProfile, tutor_id)
    if profile.profile_status not in ("approved",) and not (
        current_user.is_authenticated and (current_user.id == profile.user_id or current_user.is_admin)
    ):
        abort(404)
    reviews = [r for r in profile.reviews_received if r.moderation_status == "approved"]
    is_saved = False
    if current_user.is_authenticated and current_user.is_student:
        is_saved = any(s.tutor_profile_id == profile.id for s in current_user.saved_tutors)
    return render_template("directory/tutor_profile.html", profile=profile, reviews=reviews, is_saved=is_saved)


@directory_bp.route("/<int:tutor_id>/message", methods=["GET", "POST"])
@login_required
def message_tutor(tutor_id):
    profile = get_or_404(TutorProfile, tutor_id)
    if current_user.id == profile.user_id:
        flash("You can't message yourself.", "error")
        return redirect(url_for("directory.tutor_profile", tutor_id=tutor_id))
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            flash("Please write a message.", "error")
            return redirect(url_for("directory.message_tutor", tutor_id=tutor_id))
        convo = _get_or_create_conversation(current_user.id, profile.user_id)
        msg = Message(conversation_id=convo.id, sender_id=current_user.id,
                      recipient_id=profile.user_id, body=body)
        db.session.add(msg)
        db.session.commit()
        flash("Your message has been sent to the tutor.", "success")
        return redirect(url_for("student.messages"))
    return render_template("directory/message_tutor.html", profile=profile)


@directory_bp.route("/<int:tutor_id>/save", methods=["POST"])
@login_required
def save_tutor(tutor_id):
    profile = get_or_404(TutorProfile, tutor_id)
    if not current_user.is_student:
        flash("Only student accounts can save tutors.", "error")
        return redirect(url_for("directory.tutor_profile", tutor_id=tutor_id))
    existing = SavedTutor.query.filter_by(student_id=current_user.id, tutor_profile_id=profile.id).first()
    if existing:
        db.session.delete(existing)
        flash("Tutor removed from your saved list.", "info")
    else:
        db.session.add(SavedTutor(student_id=current_user.id, tutor_profile_id=profile.id))
        flash("Tutor saved to your list.", "success")
    db.session.commit()
    return redirect(url_for("directory.tutor_profile", tutor_id=tutor_id))


@directory_bp.route("/<int:tutor_id>/request-lesson", methods=["GET", "POST"])
@login_required
def request_lesson(tutor_id):
    profile = get_or_404(TutorProfile, tutor_id)
    if not current_user.is_student:
        flash("Only student accounts can request lessons.", "error")
        return redirect(url_for("directory.tutor_profile", tutor_id=tutor_id))
    if current_user.id == profile.user_id:
        flash("You can't book a lesson with yourself.", "error")
        return redirect(url_for("directory.tutor_profile", tutor_id=tutor_id))
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        date_str = request.form.get("date", "").strip()
        time_str = request.form.get("time", "").strip()
        notes = request.form.get("notes", "").strip()
        start_at = None
        if date_str and time_str:
            try:
                start_at = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            except ValueError:
                start_at = None
        booking = Booking(
            learner_id=current_user.id,
            tutor_id=profile.user_id,
            subject=subject or (profile.subjects[0].name if profile.subjects else "General"),
            start_at=start_at,
            status="pending",
            price=profile.hourly_rate or 0.0,
            payment_status="unpaid",
        )
        db.session.add(booking)
        # notify tutor via a message in their shared conversation
        convo = _get_or_create_conversation(current_user.id, profile.user_id)
        body = f"I'd like to book a {booking.subject} lesson"
        if start_at:
            body += f" on {start_at.strftime('%d %b %Y at %H:%M')}"
        if notes:
            body += f". {notes}"
        db.session.add(Message(conversation_id=convo.id, sender_id=current_user.id,
                               recipient_id=profile.user_id, body=body))
        db.session.commit()
        flash("Your lesson request has been sent. The tutor will confirm the booking shortly.", "success")
        return redirect(url_for("student.bookings"))
    return render_template("directory/request_lesson.html", profile=profile)


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

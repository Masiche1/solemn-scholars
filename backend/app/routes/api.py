"""JSON API endpoints for Tutorly."""
from flask import Blueprint, request, jsonify
from app.models import TutorProfile, Subject, Job
from app import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/tutors/search")
def search_tutors():
    q = request.args.get("q", "").strip()
    subject_slug = request.args.get("subject", "").strip()
    query = TutorProfile.query.filter_by(profile_status="approved")
    if subject_slug:
        subj = Subject.query.filter_by(slug=subject_slug).first()
        if subj:
            query = query.filter(TutorProfile.subjects.contains(subj))
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(TutorProfile.headline.ilike(like), TutorProfile.biography.ilike(like))
        )
    results = query.limit(20).all()
    return jsonify([
        {
            "id": t.id,
            "name": t.user.name,
            "headline": t.headline,
            "rate": t.hourly_rate,
            "rating": t.avg_rating,
            "review_count": t.review_count,
            "location": t.location_name,
            "modes": t.modes_list,
            "subjects": [s.name for s in t.subjects],
            "avatar": t.user.avatar_url,
            "verified": t.is_verified,
        }
        for t in results
    ])


@api_bp.route("/jobs/search")
def search_jobs():
    q = request.args.get("q", "").strip()
    query = Job.query.filter_by(status="open")
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Job.title.ilike(like), Job.subject.ilike(like), Job.goals.ilike(like))
        )
    jobs = query.order_by(Job.created_at.desc()).limit(20).all()
    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "subject": j.subject,
            "level": j.level,
            "mode": j.teaching_mode,
            "location": j.location,
            "budget": j.budget_label,
            "applications": j.application_count,
            "posted": j.age_label,
        }
        for j in jobs
    ])


@api_bp.route("/subjects")
def list_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return jsonify([{"id": s.id, "name": s.name, "slug": s.slug, "icon": s.icon} for s in subjects])

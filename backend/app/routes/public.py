"""Public marketing pages for Tutorly."""
from flask import Blueprint, request, redirect, url_for, render_template, flash
from app import db
from app.models import TutorProfile, Subject, Lead, Location
from app.services.helpers import slugify

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    featured = TutorProfile.query.filter_by(profile_status="approved").order_by(
        TutorProfile.completed_lessons.desc()).limit(4).all()
    subjects = Subject.query.order_by(Subject.name).all()
    # aggregate stats
    total_tutors = TutorProfile.query.filter_by(profile_status="approved").count()
    total_lessons = sum(t.completed_lessons for t in TutorProfile.query.all())
    return render_template("public/home.html", featured=featured, subjects=subjects,
                           total_tutors=total_tutors, total_lessons=total_lessons)


@public_bp.route("/find-a-tutor", methods=["GET", "POST"])
def find_a_tutor():
    if request.method == "POST":
        lead = _capture_lead(request.form, source_page="find-a-tutor")
        db.session.add(lead)
        db.session.commit()
        flash("Thanks! We'll show you matching tutors right away.", "success")
        # pass filters to directory
        return redirect(url_for("directory.directory", subject=request.form.get("subject", ""),
                                mode=request.form.get("mode", "")))
    subjects = Subject.query.order_by(Subject.name).all()
    featured = TutorProfile.query.filter_by(profile_status="approved").limit(6).all()
    return render_template("public/find_a_tutor.html", subjects=subjects, featured=featured)


@public_bp.route("/post-a-job", methods=["GET", "POST"])
def post_a_job():
    subjects = Subject.query.order_by(Subject.name).all()
    if request.method == "POST":
        lead = _capture_lead(request.form, source_page="post-a-job", job=True)
        db.session.add(lead)
        db.session.commit()
        flash("Your request is live. We'll notify you when tutors match your needs.", "success")
        return redirect(url_for("public.post_a_job"))
    return render_template("public/post_a_job.html", subjects=subjects)


@public_bp.route("/become-a-tutor", methods=["GET", "POST"])
def become_a_tutor():
    if request.method == "POST":
        # capture interest as a lead for follow-up
        lead = Lead(
            source_page="become-a-tutor",
            email=request.form.get("email", "").strip().lower(),
            name=request.form.get("name", "").strip(),
            subject=request.form.get("subjects", ""),
            consent_status="granted" if request.form.get("consent") else "denied",
            lifecycle_status="new",
        )
        db.session.add(lead)
        db.session.commit()
        flash("Thanks for your interest! Redirecting you to create your tutor account.", "success")
        return redirect(url_for("auth.signup", role="tutor"))
    return render_template("public/become_a_tutor.html")


@public_bp.route("/how-it-works")
def how_it_works():
    return render_template("public/how_it_works.html")


@public_bp.route("/subjects")
def subjects_index():
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template("public/subjects_index.html", subjects=subjects)


@public_bp.route("/subjects/<slug>")
def subject_landing(slug):
    subject = Subject.query.filter_by(slug=slug).first_or_404()
    tutors = TutorProfile.query.filter(
        TutorProfile.subjects.contains(subject),
        TutorProfile.profile_status == "approved",
    ).limit(8).all()
    return render_template("public/subject_landing.html", subject=subject, tutors=tutors)


@public_bp.route("/locations")
def locations_index():
    locations = Location.query.order_by(Location.name).all()
    return render_template("public/locations_index.html", locations=locations)


@public_bp.route("/locations/<slug>")
def location_landing(slug):
    location = Location.query.filter_by(slug=slug).first_or_404()
    tutors = TutorProfile.query.filter(
        TutorProfile.location_name == location.name,
        TutorProfile.profile_status == "approved",
    ).limit(8).all()
    subjects = Subject.query.order_by(Subject.name).limit(8).all()
    return render_template("public/location_landing.html", location=location, tutors=tutors, subjects=subjects)


@public_bp.route("/about")
def about():
    total_tutors = TutorProfile.query.filter_by(profile_status="approved").count()
    total_lessons = sum(t.completed_lessons for t in TutorProfile.query.all())
    total_subjects = Subject.query.count()
    total_locations = Location.query.count()
    return render_template("public/about.html", total_tutors=total_tutors, total_lessons=total_lessons,
                           total_subjects=total_subjects, total_locations=total_locations)


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        lead = Lead(
            source_page="contact",
            email=request.form.get("email", "").strip().lower(),
            name=request.form.get("name", "").strip(),
            consent_status="granted" if request.form.get("consent") else "denied",
            lifecycle_status="new",
        )
        lead.subject = request.form.get("message", "")[:120]
        db.session.add(lead)
        db.session.commit()
        flash("Thanks for reaching out! We'll get back to you within one business day.", "success")
        return redirect(url_for("public.contact"))
    return render_template("public/contact.html")


@public_bp.route("/privacy")
def privacy():
    return render_template("public/privacy.html")


@public_bp.route("/terms")
def terms():
    return render_template("public/terms.html")


def _capture_lead(form, source_page, job=False):
    return Lead(
        source_page=source_page,
        subject=form.get("subject", ""),
        level=form.get("level", "") or form.get("age", ""),
        location=form.get("location", ""),
        teaching_mode=form.get("mode", "") or form.get("teaching_mode", ""),
        budget=form.get("budget", "") or _budget_label(form),
        email=form.get("email", "").strip().lower(),
        phone=form.get("phone", ""),
        name=form.get("name", ""),
        consent_status="granted" if form.get("consent") else "denied",
        lifecycle_status="new",
    )


def _budget_label(form):
    bmin = form.get("budget_min")
    bmax = form.get("budget_max")
    if bmin and bmax:
        return f"${bmin}-${bmax}/hour"
    return ""

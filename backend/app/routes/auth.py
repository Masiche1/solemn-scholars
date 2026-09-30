"""User loader and auth routes for Tutorly."""
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User, TutorProfile
from app.services.helpers import slugify

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(_home_for(current_user))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if user.status != "active":
                flash("Your account is not active. Please contact support.", "error")
                return render_template("auth/login.html")
            login_user(user, remember=bool(request.form.get("remember")))
            next_url = request.args.get("next")
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(next_url or _home_for(user))
        flash("Invalid email or password.", "error")
    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(_home_for(current_user))
    if request.method == "POST":
        role = request.form.get("role", "student")
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        consent = request.form.get("consent")

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not email or "@" not in email:
            errors.append("Please enter a valid email address.")
        if User.query.filter_by(email=email).first():
            errors.append("An account with that email already exists.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if not consent:
            errors.append("Please agree to the Terms of Service and Privacy Policy.")
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("auth/signup.html", role=role, name=name, email=email)

        user = User(name=name, email=email, role=role, status="active",
                    avatar_url=f"https://i.pravatar.cc/200?u={email}")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        if role == "tutor":
            profile = TutorProfile(
                user_id=user.id,
                headline=f"New {role.title()} — completing profile",
                biography="",
                profile_status="draft",
                verification_status="unverified",
            )
            db.session.add(profile)

        db.session.commit()
        login_user(user)
        flash(f"Welcome to Tutorly, {name}! Your account is ready.", "success")
        if role == "tutor":
            return redirect(url_for("tutor.edit_profile"))
        return redirect(url_for("student.dashboard"))

    role = request.args.get("role", "student")
    return render_template("auth/signup.html", role=role)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("public.home"))


def _home_for(user):
    if user.is_admin:
        return url_for("admin.overview")
    if user.is_tutor:
        return url_for("tutor.dashboard")
    return url_for("student.dashboard")

"""Shared helper utilities for Tutorly."""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    """Restrict a view to users with one of the given roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def student_required(fn):
    return roles_required("student", "admin")(fn)


def tutor_required(fn):
    return roles_required("tutor", "admin")(fn)


def admin_required(fn):
    return roles_required("admin")(fn)


def get_or_404(model, pk):
    obj = model.query.get(pk)
    if obj is None:
        abort(404)
    return obj


def slugify(text):
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

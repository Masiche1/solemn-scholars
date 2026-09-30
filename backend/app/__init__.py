"""Tutorly - Tutor Marketplace application factory."""
import os
import secrets
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="development"):
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tutorly-dev-secret-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(os.path.dirname(__file__), "..", "..", "database", "tutorly.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MARKETPLACE_COMMISSION_PCT"] = 15
    app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_BYTES", 40 * 1024 * 1024))
    app.config["VERIFICATION_MAX_FILE_BYTES"] = int(os.environ.get("VERIFICATION_MAX_FILE_BYTES", 10 * 1024 * 1024))
    app.config["VERIFICATION_SCAN_COMMAND"] = os.environ.get("VERIFICATION_SCAN_COMMAND", "clamdscan")
    app.config["VERIFICATION_REQUIRE_SCAN"] = os.environ.get(
        "VERIFICATION_REQUIRE_SCAN", "true" if config_name == "production" else "false"
    ).lower() in ("1", "true", "yes", "on")
    app.config["VERIFICATION_SCAN_TIMEOUT_SECONDS"] = int(os.environ.get("VERIFICATION_SCAN_TIMEOUT_SECONDS", 30))
    app.config["VERIFICATION_REJECTED_RETENTION_DAYS"] = int(os.environ.get("VERIFICATION_REJECTED_RETENTION_DAYS", 30))
    app.config["VERIFICATION_APPROVED_RETENTION_DAYS"] = int(os.environ.get("VERIFICATION_APPROVED_RETENTION_DAYS", 365))
    app.config["VERIFICATION_UPLOAD_DIR"] = os.environ.get(
        "VERIFICATION_UPLOAD_DIR", os.path.join(app.instance_path, "verification_uploads")
    )
    os.makedirs(app.config["VERIFICATION_UPLOAD_DIR"], mode=0o700, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    
    # Enable CORS for Next.js frontend
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Jinja global: current year for footer
    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.utcnow().year,
            "site_name": "Solemn Scholars",
            "commission_pct": app.config["MARKETPLACE_COMMISSION_PCT"],
            "max_upload_size_mb": app.config["VERIFICATION_MAX_FILE_BYTES"] // (1024 * 1024),
        }

    @app.context_processor
    def inject_csrf_token():
        from flask import session
        token = session.get("csrf_token")
        if not token:
            token = secrets.token_urlsafe(32)
            session["csrf_token"] = token
        return {"csrf_token": lambda: token}

    # Register blueprints
    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.directory import directory_bp
    from app.routes.jobs import jobs_bp
    from app.routes.student import student_bp
    from app.routes.tutor import tutor_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.learning import learning_bp
    from app.routes.curriculum import curriculum_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(directory_bp, url_prefix="/tutors")
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(tutor_bp, url_prefix="/tutor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(learning_bp)
    app.register_blueprint(curriculum_bp)

    # Error handlers
    from app.routes.errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()
        # Only seed database if it's empty (first run)
        from app.models import User
        if User.query.count() == 0:
            from app.services.seed import seed_database
            seed_database()

    return app

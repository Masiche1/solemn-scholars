"""Database models for the Tutorly marketplace."""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import json


# ---------------------------------------------------------------------------
# Association tables
# ---------------------------------------------------------------------------
tutor_subjects = db.Table(
    "tutor_subjects",
    db.Column("tutor_profile_id", db.Integer, db.ForeignKey("tutor_profiles.id"), primary_key=True),
    db.Column("subject_id", db.Integer, db.ForeignKey("subjects.id"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------
class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    icon = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    tutor_count = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    price_from = db.Column(db.Integer, nullable=True)  # per hour in whole units
    accent = db.Column(db.String(30), nullable=True)   # CSS accent key for card theming
    image = db.Column(db.String(120), nullable=True)    # path to illustration under static/img/subjects/
    symbol = db.Column(db.String(20), nullable=True)    # short text glyph shown next to subject name
    curriculum_topic_id = db.Column(db.String(100), db.ForeignKey("topics.id"), nullable=True)  # Link to curriculum topic

    curriculum_topic = db.relationship("Topic", foreign_keys=[curriculum_topic_id])

    diagnostic_assessments = db.relationship(
        "DiagnosticAssessment",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    topic_progress = db.relationship(
        "TopicProgress",
        back_populates="subject"
    )

    question_attempts = db.relationship(
        "QuestionAttempt",
        back_populates="subject"
    )
    practice_sessions = db.relationship(
        "PracticeSession",
        back_populates="subject"
    )
    study_plans = db.relationship(
        "StudyPlan",
        back_populates="subject"
    )
    daily_tasks = db.relationship(
        "DailyTask",
        back_populates="subject"
    )
    def __repr__(self):
        return f"<Subject {self.name}>"


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Location {self.name}>"


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False, default="student")  # student|tutor|admin
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(40), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)  # nullable for demo/oauth users
    avatar_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="active")  # active|suspended|pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    tutor_profile = db.relationship("TutorProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    messages_sent = db.relationship("Message", foreign_keys="Message.sender_id", backref="sender", cascade="all, delete-orphan")
    messages_received = db.relationship("Message", foreign_keys="Message.recipient_id", backref="recipient")
    reviews_authored = db.relationship("Review", foreign_keys="Review.author_id", backref="author")
    bookings_as_learner = db.relationship("Booking", foreign_keys="Booking.learner_id", backref="learner")
    bookings_as_tutor = db.relationship("Booking", foreign_keys="Booking.tutor_id", backref="tutor")
    jobs_posted = db.relationship("Job", foreign_keys="Job.requester_id", backref="requester")
    applications = db.relationship("Application", foreign_keys="Application.tutor_id", backref="tutor_user")
    saved_tutors = db.relationship("SavedTutor", backref="student", cascade="all, delete-orphan")
    
    # Learning relationships
    learning_progress = db.relationship("LearningProgress", back_populates="user", uselist=False, cascade="all, delete-orphan")
    study_plan = db.relationship("StudyPlan", back_populates="user", uselist=False, cascade="all, delete-orphan")
    diagnostic_assessments = db.relationship("DiagnosticAssessment", back_populates="user", cascade="all, delete-orphan")
    practice_sessions = db.relationship("PracticeSession", back_populates="user", cascade="all, delete-orphan")
    question_attempts = db.relationship("QuestionAttempt", back_populates="user", cascade="all, delete-orphan")
    topic_progress = db.relationship("TopicProgress", back_populates="user", cascade="all, delete-orphan")
    daily_tasks = db.relationship("DailyTask", back_populates="user", cascade="all, delete-orphan")
    newton_conversations = db.relationship("NewtonConversation", back_populates="user", cascade="all, delete-orphan")
    tutor_recommendations = db.relationship("TutorRecommendation", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_tutor(self):
        return self.role == "tutor"

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# ---------------------------------------------------------------------------
# Tutor profile
# ---------------------------------------------------------------------------
class TutorProfile(db.Model):
    __tablename__ = "tutor_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    headline = db.Column(db.String(200), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    teaching_approach = db.Column(db.Text, nullable=True)
    qualifications = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.Integer, default=0)
    hourly_rate = db.Column(db.Float, default=35.0)
    teaching_modes = db.Column(db.String(120), default="online,in-person")  # comma separated
    location_name = db.Column(db.String(120), nullable=True)
    languages = db.Column(db.String(200), default="English")
    response_time = db.Column(db.String(60), default="within a few hours")
    verification_status = db.Column(db.String(30), default="unverified")  # unverified|pending|verified|rejected
    profile_status = db.Column(db.String(30), default="draft")  # draft|pending|approved|rejected
    completed_lessons = db.Column(db.Integer, default=0)
    repeat_learner_rate = db.Column(db.Integer, default=0)  # percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subjects = db.relationship("Subject", secondary=tutor_subjects, backref="tutors")
    availability = db.relationship("Availability", backref="tutor", cascade="all, delete-orphan")
    reviews_received = db.relationship("Review", foreign_keys="Review.recipient_id", backref="recipient", cascade="all, delete-orphan")
    verification_submissions = db.relationship("VerificationSubmission", backref="tutor_profile", cascade="all, delete-orphan", order_by="VerificationSubmission.submitted_at.desc()")
    tutor_recommendations = db.relationship("TutorRecommendation", back_populates="tutor_profile", cascade="all, delete-orphan")
    
    @property
    def modes_list(self):
        return [m.strip() for m in (self.teaching_modes or "").split(",") if m.strip()]

    @property
    def languages_list(self):
        return [l.strip() for l in (self.languages or "").split(",") if l.strip()]

    @property
    def avg_rating(self):
        approved = [r for r in self.reviews_received if r.moderation_status == "approved"]
        if not approved:
            return 0.0
        return round(sum(r.rating for r in approved) / len(approved), 1)

    @property
    def review_count(self):
        return len([r for r in self.reviews_received if r.moderation_status == "approved"])

    @property
    def is_verified(self):
        return self.verification_status == "verified"

    @property
    def is_listable(self):
        return self.profile_status == "approved"

    def __repr__(self):
        return f"<TutorProfile {self.id} user={self.user_id}>"


class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor_profiles.id"), nullable=False)
    weekday = db.Column(db.String(10), nullable=False)  # Mon..Sun
    start_time = db.Column(db.String(10), nullable=False)  # HH:MM
    end_time = db.Column(db.String(10), nullable=False)
    timezone = db.Column(db.String(40), default="UTC")
    recurring = db.Column(db.Boolean, default=True)


class VerificationSubmission(db.Model):
    __tablename__ = "verification_submissions"
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutor_profiles.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)

    documents = db.relationship("VerificationDocument", backref="submission", cascade="all, delete-orphan")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by])


class VerificationDocument(db.Model):
    __tablename__ = "verification_documents"
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("verification_submissions.id"), nullable=False, index=True)
    document_type = db.Column(db.String(30), nullable=False)
    storage_key = db.Column(db.String(255), nullable=False, unique=True)
    original_filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    rejection_reason = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    @property
    def label(self):
        return {"id": "Government-issued photo ID", "qualification": "Qualification proof",
                "background": "Background check", "selfie": "Selfie / identity confirmation"}.get(
                    self.document_type, self.document_type.replace("_", " ").title())


class VerificationAccessLog(db.Model):
    __tablename__ = "verification_access_logs"
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("verification_documents.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


# ---------------------------------------------------------------------------
# Jobs and applications
# ---------------------------------------------------------------------------
class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(120), nullable=True)
    goals = db.Column(db.Text, nullable=True)
    teaching_mode = db.Column(db.String(40), default="online")  # online|in-person|either
    location = db.Column(db.String(160), nullable=True)
    budget_min = db.Column(db.Float, nullable=True)
    budget_max = db.Column(db.Float, nullable=True)
    schedule = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.String(40), nullable=True)
    additional_details = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="open")  # open|closed|moderated|expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)

    applications = db.relationship("Application", backref="job", cascade="all, delete-orphan")

    @property
    def budget_label(self):
        if self.budget_min and self.budget_max:
            return f"${int(self.budget_min)}–${int(self.budget_max)}/hour"
        if self.budget_min:
            return f"from ${int(self.budget_min)}/hour"
        return "Budget to be discussed"

    @property
    def application_count(self):
        return len(self.applications)

    @property
    def age_label(self):
        delta = datetime.utcnow() - self.created_at
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            return "just now"
        if hours < 24:
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        days = hours // 24
        return f"{days} day{'s' if days != 1 else ''} ago"


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    proposed_rate = db.Column(db.Float, nullable=True)
    availability_note = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending|accepted|declined|withdrawn
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Messaging
# ---------------------------------------------------------------------------
class Conversation(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True)
    participant_a_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    participant_b_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    participant_a = db.relationship("User", foreign_keys=[participant_a_id], backref="conversations_a")
    participant_b = db.relationship("User", foreign_keys=[participant_b_id], backref="conversations_b")
    messages = db.relationship("Message", backref="conversation", cascade="all, delete-orphan",
                               order_by="Message.created_at")

    def other_participant(self, user_id):
        return self.participant_b_id if self.participant_a_id == user_id else self.participant_a_id


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Bookings & reviews
# ---------------------------------------------------------------------------
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=True)
    subject = db.Column(db.String(120), nullable=True)
    start_at = db.Column(db.DateTime, nullable=True)
    end_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending|confirmed|completed|cancelled
    price = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default="unpaid")  # unpaid|paid|refunded
    meeting_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    review = db.relationship("Review", backref="booking", uselist=False)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("tutor_profiles.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    moderation_status = db.Column(db.String(20), default="approved")  # approved|pending|flagged|removed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Leads (marketing)
# ---------------------------------------------------------------------------
class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    source_page = db.Column(db.String(120), nullable=True)
    subject = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(160), nullable=True)
    teaching_mode = db.Column(db.String(40), nullable=True)
    budget = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(40), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    consent_status = db.Column(db.String(30), default="granted")
    lifecycle_status = db.Column(db.String(30), default="new")  # new|contacted|matched|converted|lost
    assigned_to = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Saved tutors (student wishlist)
# ---------------------------------------------------------------------------
class SavedTutor(db.Model):
    __tablename__ = "saved_tutors"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tutor_profile_id = db.Column(db.Integer, db.ForeignKey("tutor_profiles.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tutor_profile = db.relationship("TutorProfile")


# ---------------------------------------------------------------------------
# Learning & Diagnostics (Revisions Hub integration)
# ---------------------------------------------------------------------------
class DiagnosticAssessment(db.Model):
    __tablename__ = "diagnostic_assessments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    assessment_type = db.Column(db.String(50), nullable=False)  # initial, progress, final
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    accuracy_percentage = db.Column(db.Float, default=0.0)
    topics_mastered = db.Column(db.Text, nullable=True)  # JSON array of topic IDs
    topics_struggling = db.Column(db.Text, nullable=True)  # JSON array of topic IDs
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="diagnostic_assessments")
    subject = db.relationship("Subject", back_populates="diagnostic_assessments")
    question_attempts = db.relationship("QuestionAttempt", back_populates="diagnostic", cascade="all, delete-orphan")
    
    @property
    def is_completed(self):
        return self.completed_at is not None
    
    def __repr__(self):
        return f"<DiagnosticAssessment {self.id} user={self.user_id} type={self.assessment_type}>"


class LearningProgress(db.Model):
    __tablename__ = "learning_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    total_practice_time_minutes = db.Column(db.Integer, default=0)
    total_questions_attempted = db.Column(db.Integer, default=0)
    total_correct_answers = db.Column(db.Integer, default=0)
    overall_accuracy = db.Column(db.Float, default=0.0)
    last_practice_date = db.Column(db.DateTime, nullable=True)
    current_level = db.Column(db.String(50), default="beginner")  # beginner, intermediate, advanced
    xp_points = db.Column(db.Integer, default=0)
    badges_earned = db.Column(db.Text, nullable=True)  # JSON array of badge IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship("User", back_populates="learning_progress", uselist=False)
   
    @property
    def accuracy_percentage(self):
        if self.total_questions_attempted == 0:
            return 0.0
        return round((self.total_correct_answers / self.total_questions_attempted) * 100, 1)
    
    def __repr__(self):
        return f"<LearningProgress user={self.user_id} streak={self.current_streak}>"


class TopicProgress(db.Model):
    __tablename__ = "topic_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    topic_name = db.Column(db.String(120), nullable=False)
    topic_code = db.Column(db.String(50), nullable=True)  # standardized topic identifier
    mastery_level = db.Column(db.Float, default=0.0)  # 0-100 percentage
    questions_attempted = db.Column(db.Integer, default=0)
    questions_correct = db.Column(db.Integer, default=0)
    last_practiced = db.Column(db.DateTime, nullable=True)
    recommended_priority = db.Column(db.String(20), default="normal")  # high, normal, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship("User", back_populates="topic_progress")
    subject = db.relationship("Subject", back_populates="topic_progress")
    
    @property
    def accuracy(self):
        if self.questions_attempted == 0:
            return 0.0
        return round((self.questions_correct / self.questions_attempted) * 100, 1)
    
    def __repr__(self):
        return f"<TopicProgress user={self.user_id} topic={self.topic_name} mastery={self.mastery_level}%>"


class PracticeSession(db.Model):
    __tablename__ = "practice_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    topic_focus = db.Column(db.String(120), nullable=True)
    session_type = db.Column(db.String(50), default="practice")  # practice, diagnostic, exam, remediation
    total_questions = db.Column(db.Integer, default=0)
    completed_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="in_progress")  # in_progress, completed, abandoned
    
    user = db.relationship("User", back_populates="practice_sessions")
    subject = db.relationship("Subject", back_populates="practice_sessions")
    question_attempts = db.relationship("QuestionAttempt", back_populates="session", cascade="all, delete-orphan")
    newton_conversations = db.relationship(
    "NewtonConversation",
    back_populates="session",
    cascade="all, delete-orphan"
    )

    @property
    def completion_percentage(self):
        if self.total_questions == 0:
            return 0.0
        return round((self.completed_questions / self.total_questions) * 100, 1)
    
    @property
    def session_accuracy(self):
        if self.completed_questions == 0:
            return 0.0
        return round((self.correct_answers / self.completed_questions) * 100, 1)
    
    def __repr__(self):
        return f"<PracticeSession {self.id} user={self.user_id} type={self.session_type}>"


class QuestionAttempt(db.Model):
    __tablename__ = "question_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("practice_sessions.id"), nullable=True)
    diagnostic_id = db.Column(db.Integer, db.ForeignKey("diagnostic_assessments.id"), nullable=True)
    question_id = db.Column(db.String(100), nullable=False)  # external question identifier
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    topic = db.Column(db.String(120), nullable=True)
    question_text = db.Column(db.Text, nullable=True)
    user_answer = db.Column(db.Text, nullable=True)
    correct_answer = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)
    time_spent_seconds = db.Column(db.Integer, default=0)
    hints_used = db.Column(db.Integer, default=0)
    difficulty_level = db.Column(db.String(20), nullable=True)  # easy, medium, hard
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="question_attempts")
    subject = db.relationship("Subject", back_populates="question_attempts")
    diagnostic = db.relationship(
    "DiagnosticAssessment",
    back_populates="question_attempts"
    )
    session = db.relationship(
    "PracticeSession",
    back_populates="question_attempts"
    )
    def __repr__(self):
        return f"<QuestionAttempt {self.id} user={self.user_id} correct={self.is_correct}>"


class StudyPlan(db.Model):
    __tablename__ = "study_plans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True)
    plan_name = db.Column(db.String(120), nullable=True)
    primary_focus_subject = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    weekly_goal_hours = db.Column(db.Integer, default=5)
    current_week = db.Column(db.Integer, default=1)
    total_weeks = db.Column(db.Integer, default=8)
    priority_topics = db.Column(db.Text, nullable=True)  # JSON array of topic codes
    generated_from_diagnostic = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship("User", back_populates="study_plan", uselist=False)
    subject = db.relationship("Subject", back_populates="study_plans")
    daily_tasks = db.relationship("DailyTask", back_populates="study_plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<StudyPlan user={self.user_id} week={self.current_week}/{self.total_weeks}>"


class DailyTask(db.Model):
    __tablename__ = "daily_tasks"
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey("study_plans.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # practice, review, diagnostic, reading
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    topic = db.Column(db.String(120), nullable=True)
    target_questions = db.Column(db.Integer, default=10)
    completed_questions = db.Column(db.Integer, default=0)
    duration_minutes = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default="pending")  # pending, in_progress, completed, skipped
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="daily_tasks")
    subject = db.relationship("Subject", back_populates="daily_tasks")
    study_plan = db.relationship("StudyPlan", back_populates="daily_tasks")
    
    @property
    def completion_percentage(self):
        if self.target_questions == 0:
            return 0.0
        return round((self.completed_questions / self.target_questions) * 100, 1)
    
    def __repr__(self):
        return f"<DailyTask {self.id} date={self.scheduled_date} status={self.status}>"


class NewtonConversation(db.Model):
    __tablename__ = "newton_conversations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey("practice_sessions.id"), nullable=True)
    conversation_type = db.Column(db.String(50), default="general")  # general, question_help, concept_explanation
    topic_context = db.Column(db.String(120), nullable=True)
    total_messages = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="newton_conversations")
    session = db.relationship("PracticeSession", back_populates="newton_conversations")
    messages = db.relationship("NewtonMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NewtonConversation {self.id} user={self.user_id}>"


class NewtonMessage(db.Model):
    __tablename__ = "newton_messages"
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("newton_conversations.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), nullable=True)  # text, hint, explanation, encouragement
    question_context = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    conversation = db.relationship("NewtonConversation", back_populates="messages")
    
    def __repr__(self):
        return f"<NewtonMessage {self.id} role={self.role}>"


class TutorRecommendation(db.Model):
    __tablename__ = "tutor_recommendations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    tutor_profile_id = db.Column(db.Integer, db.ForeignKey("tutor_profiles.id"), nullable=False)
    topic_trigger = db.Column(db.String(120), nullable=True)  # Topic that triggered recommendation
    match_score = db.Column(db.Float, default=0.0)  # 0-100 compatibility score
    recommendation_reason = db.Column(db.Text, nullable=True)
    triggered_by_diagnostic = db.Column(db.Boolean, default=False)
    accuracy_threshold = db.Column(db.Float, nullable=True)  # User's accuracy that triggered this
    view_count = db.Column(db.Integer, default=0)
    contacted = db.Column(db.Boolean, default=False)
    contacted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="tutor_recommendations")
    tutor_profile = db.relationship("TutorProfile", back_populates="tutor_recommendations")
    
    def __repr__(self):
        return f"<TutorRecommendation user={self.user_id} tutor={self.tutor_profile_id} score={self.match_score}%>"


# ---------------------------------------------------------------------------
# Curriculum Content Models (Revisions Hub integration)
# ---------------------------------------------------------------------------
class Programme(db.Model):
    __tablename__ = "programmes"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    ages = db.Column(db.String(50), nullable=True)
    curriculum_model = db.Column(db.String(120), nullable=True)
    programme_meta = db.Column(db.Text, nullable=True)  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subject_groups = db.relationship("SubjectGroup", backref="programme", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Programme {self.id} {self.name}>"


class SubjectGroup(db.Model):
    __tablename__ = "subject_groups"
    id = db.Column(db.String(50), primary_key=True)
    programme_id = db.Column(db.String(50), db.ForeignKey("programmes.id"), nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(50), nullable=False)  # subject_group | learning_area
    description = db.Column(db.Text, nullable=True)
    depth_tier = db.Column(db.String(20), nullable=False)  # full | lean | scaffold
    discipline = db.Column(db.String(50), nullable=True)
    accent_color = db.Column(db.String(50), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    
    strands = db.relationship("Strand", backref="subject_group", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SubjectGroup {self.id} {self.name}>"


class Strand(db.Model):
    __tablename__ = "strands"
    id = db.Column(db.String(50), primary_key=True)
    programme_id = db.Column(db.String(50), db.ForeignKey("programmes.id"), nullable=False)
    subject_group_id = db.Column(db.String(50), db.ForeignKey("subject_groups.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    spec_ref = db.Column(db.String(200), nullable=True)
    topic_count = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0)
    
    topics = db.relationship("Topic", backref="strand", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Strand {self.id} {self.name}>"


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.String(100), primary_key=True)
    programme_id = db.Column(db.String(50), db.ForeignKey("programmes.id"), nullable=False)
    subject_group_id = db.Column(db.String(50), db.ForeignKey("subject_groups.id"), nullable=False)
    strand_id = db.Column(db.String(50), db.ForeignKey("strands.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    key_concepts = db.Column(db.Text, nullable=True)  # JSON array
    related_concepts = db.Column(db.Text, nullable=True)  # JSON array
    concepts = db.Column(db.Text, nullable=True)  # JSON array
    global_context_links = db.Column(db.Text, nullable=True)  # JSON array
    atl_links = db.Column(db.Text, nullable=True)  # JSON array
    criteria_focus = db.Column(db.Text, nullable=True)  # JSON array
    depth_tier = db.Column(db.String(20), nullable=False)  # full | lean | scaffold
    vocabulary = db.Column(db.Text, nullable=True)  # JSON array of {term, definition}
    learning_objectives = db.Column(db.Text, nullable=True)  # JSON object
    progression = db.Column(db.Text, nullable=True)  # JSON array
    misconceptions = db.Column(db.Text, nullable=True)  # JSON array
    skills_graph = db.Column(db.Text, nullable=True)  # JSON object
    lesson_engine = db.Column(db.Text, nullable=True)  # JSON object
    practice_seeds = db.Column(db.Text, nullable=True)  # JSON array
    newton_prompts = db.Column(db.Text, nullable=True)  # JSON array
    uoi_links = db.Column(db.Text, nullable=True)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    question_bank = db.relationship("QuestionBankItem", backref="topic", cascade="all, delete-orphan")
    
    @property
    def key_concepts_list(self):
        return json.loads(self.key_concepts) if self.key_concepts else []
    
    @property
    def vocabulary_list(self):
        return json.loads(self.vocabulary) if self.vocabulary else []
    
    @property
    def progression_list(self):
        return json.loads(self.progression) if self.progression else []
    
    def __repr__(self):
        return f"<Topic {self.id} {self.name}>"


class QuestionBankItem(db.Model):
    __tablename__ = "question_bank_items"
    id = db.Column(db.String(100), primary_key=True)
    topic_id = db.Column(db.String(100), db.ForeignKey("topics.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # multiple_choice, short_answer, essay, etc.
    difficulty_level = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    correct_answer = db.Column(db.Text, nullable=True)
    options = db.Column(db.Text, nullable=True)  # JSON array for multiple choice
    explanation = db.Column(db.Text, nullable=True)
    hints = db.Column(db.Text, nullable=True)  # JSON array
    marks = db.Column(db.Integer, default=1)
    subject_tag = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.Text, nullable=True)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def options_list(self):
        return json.loads(self.options) if self.options else []
    
    @property
    def hints_list(self):
        return json.loads(self.hints) if self.hints else []
    
    def __repr__(self):
        return f"<QuestionBankItem {self.id} {self.question_type}>"

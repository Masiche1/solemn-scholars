"""
Database migration script to add learning/diagnostic tables and curriculum content models 
to existing Tutors Hub database.
Run this script to update the database schema for Solemn Scholars integration.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    DiagnosticAssessment, LearningProgress, TopicProgress, PracticeSession,
    QuestionAttempt, StudyPlan, DailyTask, NewtonConversation, NewtonMessage,
    TutorRecommendation, Programme, SubjectGroup, Strand, Topic, QuestionBankItem
)

def migrate_database():
    """Create all new learning-related and curriculum tables in the database."""
    app = create_app()
    
    with app.app_context():
        print("Starting database migration for Solemn Scholars...")
        
        # Create learning tables
        learning_tables = [
            DiagnosticAssessment,
            LearningProgress,
            TopicProgress,
            PracticeSession,
            QuestionAttempt,
            StudyPlan,
            DailyTask,
            NewtonConversation,
            NewtonMessage,
            TutorRecommendation
        ]
        
        print("\nCreating learning tables...")
        for table in learning_tables:
            try:
                table.__table__.create(db.engine, checkfirst=True)
                print(f"[OK] Created table: {table.__tablename__}")
            except Exception as e:
                print(f"[ERROR] Error creating table {table.__tablename__}: {e}")
        
        # Create curriculum tables
        curriculum_tables = [
            Programme,
            SubjectGroup,
            Strand,
            Topic,
            QuestionBankItem
        ]
        
        print("\nCreating curriculum tables...")
        for table in curriculum_tables:
            try:
                table.__table__.create(db.engine, checkfirst=True)
                print(f"[OK] Created table: {table.__tablename__}")
            except Exception as e:
                print(f"[ERROR] Error creating table {table.__tablename__}: {e}")
        
        print("\n[SUCCESS] Migration completed successfully!")
        print("\nLearning tables added:")
        print("- diagnostic_assessments")
        print("- learning_progress")
        print("- topic_progress")
        print("- practice_sessions")
        print("- question_attempts")
        print("- study_plans")
        print("- daily_tasks")
        print("- newton_conversations")
        print("- newton_messages")
        print("- tutor_recommendations")
        
        print("\nCurriculum tables added:")
        print("- programmes")
        print("- subject_groups")
        print("- strands")
        print("- topics")
        print("- question_bank_items")
        
        print("\n[NEXT] Run curriculum seeder to populate content")
        print("   python scripts/seed_curriculum.py")

if __name__ == "__main__":
    migrate_database()

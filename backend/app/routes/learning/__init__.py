"""
Learning API Blueprint - Revisions Hub integration endpoints
Provides REST API for diagnostic assessments, learning progress, practice sessions,
study plans, and AI tutor recommendations.
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import (
    LearningProgress, TopicProgress, PracticeSession, QuestionAttempt,
    DiagnosticAssessment, StudyPlan, DailyTask, NewtonConversation, NewtonMessage,
    TutorRecommendation, User, TutorProfile, Subject
)
import json
from datetime import datetime, timedelta

learning_bp = Blueprint('learning', __name__, url_prefix='/api/learning')

@learning_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for learning API."""
    return jsonify({'status': 'healthy', 'service': 'learning-api'})

# ---------------------------------------------------------------------------
# Learning Progress Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/progress', methods=['GET'])
@login_required
def get_learning_progress():
    """Get current user's learning progress."""
    progress = LearningProgress.query.filter_by(user_id=current_user.id).first()
    
    if not progress:
        # Create initial progress record
        progress = LearningProgress(user_id=current_user.id)
        db.session.add(progress)
        db.session.commit()
    
    return jsonify({
        'current_streak': progress.current_streak,
        'longest_streak': progress.longest_streak,
        'total_practice_time_minutes': progress.total_practice_time_minutes,
        'total_questions_attempted': progress.total_questions_attempted,
        'total_correct_answers': progress.total_correct_answers,
        'overall_accuracy': progress.accuracy_percentage,
        'last_practice_date': progress.last_practice_date.isoformat() if progress.last_practice_date else None,
        'current_level': progress.current_level,
        'xp_points': progress.xp_points,
        'badges_earned': json.loads(progress.badges_earned) if progress.badges_earned else []
    })


@learning_bp.route('/progress/topic', methods=['GET'])
@login_required
def get_topic_progress():
    """Get user's progress by topic."""
    subject_id = request.args.get('subject_id', type=int)
    
    query = TopicProgress.query.filter_by(user_id=current_user.id)
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    
    topics = query.order_by(TopicProgress.mastery_level.asc()).all()
    
    return jsonify([{
        'id': t.id,
        'subject_id': t.subject_id,
        'topic_name': t.topic_name,
        'topic_code': t.topic_code,
        'mastery_level': t.mastery_level,
        'questions_attempted': t.questions_attempted,
        'questions_correct': t.questions_correct,
        'accuracy': t.accuracy,
        'last_practiced': t.last_practiced.isoformat() if t.last_practiced else None,
        'recommended_priority': t.recommended_priority
    } for t in topics])


# ---------------------------------------------------------------------------
# Practice Session Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/practice/start', methods=['POST'])
@login_required
def start_practice_session():
    """Start a new practice session."""
    data = request.get_json()
    
    session = PracticeSession(
        user_id=current_user.id,
        subject_id=data.get('subject_id'),
        topic_focus=data.get('topic_focus'),
        session_type=data.get('session_type', 'practice'),
        total_questions=data.get('total_questions', 10)
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'session_id': session.id,
        'started_at': session.started_at.isoformat()
    }), 201


@learning_bp.route('/practice/<int:session_id>/submit', methods=['POST'])
@login_required
def submit_question_attempt(session_id):
    """Submit a question attempt within a practice session."""
    data = request.get_json()
    
    session = PracticeSession.query.get_or_404(session_id)
    if session.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    attempt = QuestionAttempt(
        user_id=current_user.id,
        session_id=session_id,
        question_id=data['question_id'],
        subject_id=data.get('subject_id'),
        topic=data.get('topic'),
        question_text=data.get('question_text'),
        user_answer=data['user_answer'],
        correct_answer=data.get('correct_answer'),
        is_correct=data.get('is_correct'),
        time_spent_seconds=data.get('time_spent_seconds', 0),
        hints_used=data.get('hints_used', 0),
        difficulty_level=data.get('difficulty_level')
    )
    
    db.session.add(attempt)
    
    # Update session stats
    session.completed_questions += 1
    if attempt.is_correct:
        session.correct_answers += 1
    
    # Update topic progress
    if attempt.topic:
        topic_progress = TopicProgress.query.filter_by(
            user_id=current_user.id,
            topic_name=attempt.topic
        ).first()
        
        if not topic_progress:
            topic_progress = TopicProgress(
                user_id=current_user.id,
                subject_id=attempt.subject_id,
                topic_name=attempt.topic,
                topic_code=data.get('topic_code')
            )
            db.session.add(topic_progress)
        
        topic_progress.questions_attempted += 1
        if attempt.is_correct:
            topic_progress.questions_correct += 1
        topic_progress.last_practiced = datetime.utcnow()
        topic_progress.mastery_level = topic_progress.accuracy
    
    # Update overall learning progress
    progress = LearningProgress.query.filter_by(user_id=current_user.id).first()
    if not progress:
        progress = LearningProgress(user_id=current_user.id)
        db.session.add(progress)
    
    progress.total_questions_attempted += 1
    if attempt.is_correct:
        progress.total_correct_answers += 1
    progress.last_practice_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'attempt_id': attempt.id,
        'is_correct': attempt.is_correct,
        'session_progress': {
            'completed': session.completed_questions,
            'total': session.total_questions,
            'accuracy': session.session_accuracy
        }
    })


@learning_bp.route('/practice/<int:session_id>/complete', methods=['POST'])
@login_required
def complete_practice_session(session_id):
    """Complete a practice session."""
    session = PracticeSession.query.get_or_404(session_id)
    if session.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    session.completed_at = datetime.utcnow()
    session.status = 'completed'
    session.time_spent_minutes = data.get('time_spent_minutes', 0)
    
    # Update learning progress
    progress = LearningProgress.query.filter_by(user_id=current_user.id).first()
    if progress:
        progress.total_practice_time_minutes += session.time_spent_minutes
        
        # Update streak if practiced today
        if progress.last_practice_date and progress.last_practice_date.date() == datetime.utcnow().date():
            progress.current_streak += 1
            if progress.current_streak > progress.longest_streak:
                progress.longest_streak = progress.current_streak
        else:
            progress.current_streak = 1
    
    db.session.commit()
    
    return jsonify({
        'session_id': session.id,
        'completed_at': session.completed_at.isoformat(),
        'total_correct': session.correct_answers,
        'total_questions': session.completed_questions,
        'accuracy': session.session_accuracy,
        'time_spent_minutes': session.time_spent_minutes
    })


# ---------------------------------------------------------------------------
# Diagnostic Assessment Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/diagnostic/start', methods=['POST'])
@login_required
def start_diagnostic():
    """Start a diagnostic assessment."""
    data = request.get_json()
    
    diagnostic = DiagnosticAssessment(
        user_id=current_user.id,
        subject_id=data.get('subject_id'),
        assessment_type=data.get('assessment_type', 'initial'),
        total_questions=data.get('total_questions', 20)
    )
    
    db.session.add(diagnostic)
    db.session.commit()
    
    return jsonify({
        'diagnostic_id': diagnostic.id,
        'started_at': diagnostic.started_at.isoformat()
    }), 201


@learning_bp.route('/diagnostic/<int:diagnostic_id>/complete', methods=['POST'])
@login_required
def complete_diagnostic(diagnostic_id):
    """Complete a diagnostic assessment and generate tutor recommendations."""
    diagnostic = DiagnosticAssessment.query.get_or_404(diagnostic_id)
    if diagnostic.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    diagnostic.completed_at = datetime.utcnow()
    diagnostic.correct_answers = data.get('correct_answers', 0)
    diagnostic.accuracy_percentage = diagnostic.correct_answers / diagnostic.total_questions * 100 if diagnostic.total_questions > 0 else 0
    diagnostic.topics_mastered = json.dumps(data.get('topics_mastered', []))
    diagnostic.topics_struggling = json.dumps(data.get('topics_struggling', []))
    
    # Generate tutor recommendations for struggling topics
    struggling_topics = json.loads(diagnostic.topics_struggling) if diagnostic.topics_struggling else []
    
    if struggling_topics and diagnostic.subject_id:
        generate_tutor_recommendations(current_user.id, diagnostic.subject_id, struggling_topics, diagnostic.accuracy_percentage)
    
    db.session.commit()
    
    return jsonify({
        'diagnostic_id': diagnostic.id,
        'accuracy': diagnostic.accuracy_percentage,
        'topics_struggling': struggling_topics,
        'recommendations_generated': len(struggling_topics) > 0
    })


def generate_tutor_recommendations(user_id, subject_id, struggling_topics, accuracy):
    """Generate tutor recommendations based on diagnostic results."""
    # Find tutors who teach the subject
    from app.models import tutor_subjects
    
    subject_tutors = db.session.query(TutorProfile).join(
        tutor_subjects,
        tutor_subjects.c.tutor_profile_id == TutorProfile.id
    ).filter(
        tutor_subjects.c.subject_id == subject_id,
        TutorProfile.profile_status == 'approved',
        TutorProfile.verification_status == 'verified'
    ).all()
    
    for topic in struggling_topics[:3]:  # Recommend for top 3 struggling topics
        for tutor in subject_tutors[:5]:  # Top 5 tutors per topic
            # Calculate match score based on various factors
            match_score = calculate_tutor_match_score(tutor, accuracy, topic)
            
            if match_score > 70:  # Only recommend high matches
                recommendation = TutorRecommendation(
                    user_id=user_id,
                    tutor_profile_id=tutor.id,
                    topic_trigger=topic,
                    match_score=match_score,
                    recommendation_reason=f"Struggling with {topic}. {tutor.user.name} specializes in this area with {tutor.avg_rating}★ rating.",
                    triggered_by_diagnostic=True,
                    accuracy_threshold=accuracy
                )
                db.session.add(recommendation)


def calculate_tutor_match_score(tutor, user_accuracy, topic):
    """Calculate a match score between student and tutor."""
    base_score = 75
    
    # Adjust based on tutor rating
    if tutor.avg_rating >= 4.8:
        base_score += 15
    elif tutor.avg_rating >= 4.5:
        base_score += 10
    elif tutor.avg_rating >= 4.0:
        base_score += 5
    
    # Adjust based on experience
    if tutor.years_experience >= 5:
        base_score += 10
    elif tutor.years_experience >= 2:
        base_score += 5
    
    # Adjust based on lesson count
    if tutor.completed_lessons >= 50:
        base_score += 5
    
    return min(base_score, 98)  # Cap at 98%


# ---------------------------------------------------------------------------
# Tutor Recommendations Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/recommendations', methods=['GET'])
@login_required
def get_tutor_recommendations():
    """Get personalized tutor recommendations."""
    recommendations = TutorRecommendation.query.filter_by(
        user_id=current_user.id
    ).order_by(TutorRecommendation.match_score.desc()).limit(10).all()
    
    result = []
    for rec in recommendations:
        tutor = rec.tutor_profile
        result.append({
            'recommendation_id': rec.id,
            'tutor_id': tutor.id,
            'tutor_name': tutor.user.name,
            'tutor_headline': tutor.headline,
            'hourly_rate': tutor.hourly_rate,
            'rating': tutor.avg_rating,
            'review_count': tutor.review_count,
            'match_score': rec.match_score,
            'topic_trigger': rec.topic_trigger,
            'recommendation_reason': rec.recommendation_reason,
            'triggered_by_diagnostic': rec.triggered_by_diagnostic,
            'contacted': rec.contacted
        })
    
    return jsonify(result)


@learning_bp.route('/recommendations/<int:rec_id>/contact', methods=['POST'])
@login_required
def contact_tutor_from_recommendation(rec_id):
    """Mark a tutor recommendation as contacted."""
    recommendation = TutorRecommendation.query.get_or_404(rec_id)
    if recommendation.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    recommendation.contacted = True
    recommendation.contacted_at = datetime.utcnow()
    recommendation.view_count += 1
    
    db.session.commit()
    
    return jsonify({'success': True, 'contacted_at': recommendation.contacted_at.isoformat()})


# ---------------------------------------------------------------------------
# Study Plan Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/study-plan', methods=['GET'])
@login_required
def get_study_plan():
    """Get user's current study plan."""
    plan = StudyPlan.query.filter_by(user_id=current_user.id).first()
    
    if not plan:
        return jsonify({'plan': None})
    
    # Get upcoming tasks
    upcoming_tasks = DailyTask.query.filter(
        DailyTask.user_id == current_user.id,
        DailyTask.scheduled_date >= datetime.utcnow().date(),
        DailyTask.status == 'pending'
    ).order_by(DailyTask.scheduled_date).limit(7).all()
    
    return jsonify({
        'plan': {
            'id': plan.id,
            'plan_name': plan.plan_name,
            'primary_focus_subject': plan.primary_focus_subject,
            'weekly_goal_hours': plan.weekly_goal_hours,
            'current_week': plan.current_week,
            'total_weeks': plan.total_weeks,
            'priority_topics': json.loads(plan.priority_topics) if plan.priority_topics else [],
            'generated_from_diagnostic': plan.generated_from_diagnostic
        },
        'upcoming_tasks': [{
            'id': task.id,
            'scheduled_date': task.scheduled_date.isoformat(),
            'task_type': task.task_type,
            'subject_id': task.subject_id,
            'topic': task.topic,
            'target_questions': task.target_questions,
            'duration_minutes': task.duration_minutes,
            'status': task.status
        } for task in upcoming_tasks]
    })


@learning_bp.route('/study-plan', methods=['POST'])
@login_required
def create_study_plan():
    """Create or update study plan."""
    data = request.get_json()
    
    plan = StudyPlan.query.filter_by(user_id=current_user.id).first()
    
    if plan:
        # Update existing plan
        plan.plan_name = data.get('plan_name', plan.plan_name)
        plan.primary_focus_subject = data.get('primary_focus_subject')
        plan.weekly_goal_hours = data.get('weekly_goal_hours', plan.weekly_goal_hours)
        plan.priority_topics = json.dumps(data.get('priority_topics', []))
        plan.generated_from_diagnostic = data.get('generated_from_diagnostic', False)
    else:
        # Create new plan
        plan = StudyPlan(
            user_id=current_user.id,
            plan_name=data.get('plan_name', 'My Study Plan'),
            primary_focus_subject=data.get('primary_focus_subject'),
            weekly_goal_hours=data.get('weekly_goal_hours', 5),
            priority_topics=json.dumps(data.get('priority_topics', [])),
            generated_from_diagnostic=data.get('generated_from_diagnostic', False)
        )
        db.session.add(plan)
    
    db.session.commit()
    
    return jsonify({'success': True, 'plan_id': plan.id}), 201


# ---------------------------------------------------------------------------
# Newton AI Tutor Endpoints
# ---------------------------------------------------------------------------

@learning_bp.route('/newton/conversation', methods=['POST'])
@login_required
def start_newton_conversation():
    """Start a new Newton AI conversation."""
    data = request.get_json()
    
    conversation = NewtonConversation(
        user_id=current_user.id,
        session_id=data.get('session_id'),
        conversation_type=data.get('conversation_type', 'general'),
        topic_context=data.get('topic_context')
    )
    
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'conversation_id': conversation.id,
        'started_at': conversation.started_at.isoformat()
    }), 201


@learning_bp.route('/newton/<int:conversation_id>/message', methods=['POST'])
@login_required
def send_newton_message(conversation_id):
    """Send a message to Newton AI and get response."""
    conversation = NewtonConversation.query.get_or_404(conversation_id)
    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Save user message
    user_message = NewtonMessage(
        conversation_id=conversation_id,
        role='user',
        content=data['message'],
        message_type='text',
        question_context=data.get('question_context')
    )
    db.session.add(user_message)
    
    # Generate AI response (placeholder - integrate with actual AI service)
    ai_response = generate_newton_response(data['message'], data.get('question_context'))
    
    # Save AI response
    ai_message = NewtonMessage(
        conversation_id=conversation_id,
        role='assistant',
        content=ai_response,
        message_type=data.get('message_type', 'explanation'),
        question_context=data.get('question_context')
    )
    db.session.add(ai_message)
    
    conversation.total_messages += 2
    db.session.commit()
    
    return jsonify({
        'user_message_id': user_message.id,
        'ai_message_id': ai_message.id,
        'ai_response': ai_response
    })


def generate_newton_response(user_message, question_context):
    """Generate Newton AI response (placeholder for actual AI integration)."""
    # This would integrate with your AI service
    # For now, return a helpful placeholder response
    if question_context:
        return f"I understand you're working on {question_context}. Let me help you with that. Could you provide more details about what specifically you're struggling with?"
    return "I'm here to help you understand the concept better. Can you tell me more about what you're finding difficult?"

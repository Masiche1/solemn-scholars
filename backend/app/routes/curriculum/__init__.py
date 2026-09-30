"""
Curriculum API Blueprint - Revisions Hub curriculum content endpoints
Provides REST API for programmes, subject groups, strands, topics, and question bank.
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Programme, SubjectGroup, Strand, Topic, QuestionBankItem
import json

curriculum_bp = Blueprint('curriculum', __name__, url_prefix='/api/curriculum')

# ---------------------------------------------------------------------------
# Programme Endpoints
# ---------------------------------------------------------------------------

@curriculum_bp.route('/programmes', methods=['GET'])
def get_programmes():
    """Get all available programmes."""
    programmes = Programme.query.all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'full_name': p.full_name,
        'ages': p.ages,
        'curriculum_model': p.curriculum_model,
        'programme_meta': json.loads(p.programme_meta) if p.programme_meta else {}
    } for p in programmes])


@curriculum_bp.route('/programmes/<string:programme_id>', methods=['GET'])
def get_programme(programme_id):
    """Get details of a specific programme."""
    programme = Programme.query.get_or_404(programme_id)
    
    return jsonify({
        'id': programme.id,
        'name': programme.name,
        'full_name': programme.full_name,
        'ages': programme.ages,
        'curriculum_model': programme.curriculum_model,
        'programme_meta': json.loads(programme.programme_meta) if programme.programme_meta else {},
        'subject_groups': [{
            'id': sg.id,
            'name': sg.name,
            'slug': sg.slug,
            'kind': sg.kind,
            'depth_tier': sg.depth_tier
        } for sg in programme.subject_groups]
    })


# ---------------------------------------------------------------------------
# Subject Group Endpoints
# ---------------------------------------------------------------------------

@curriculum_bp.route('/subject-groups', methods=['GET'])
def get_subject_groups():
    """Get all subject groups, optionally filtered by programme."""
    programme_id = request.args.get('programme_id')
    
    query = SubjectGroup.query
    if programme_id:
        query = query.filter_by(programme_id=programme_id)
    
    subject_groups = query.order_by(SubjectGroup.sort_order).all()
    
    return jsonify([{
        'id': sg.id,
        'programme_id': sg.programme_id,
        'slug': sg.slug,
        'name': sg.name,
        'kind': sg.kind,
        'description': sg.description,
        'depth_tier': sg.depth_tier,
        'discipline': sg.discipline,
        'accent_color': sg.accent_color,
        'sort_order': sg.sort_order,
        'strand_count': len(sg.strands)
    } for sg in subject_groups])


@curriculum_bp.route('/subject-groups/<string:sg_id>', methods=['GET'])
def get_subject_group(sg_id):
    """Get details of a specific subject group."""
    subject_group = SubjectGroup.query.get_or_404(sg_id)
    
    return jsonify({
        'id': subject_group.id,
        'programme_id': subject_group.programme_id,
        'slug': subject_group.slug,
        'name': subject_group.name,
        'kind': subject_group.kind,
        'description': subject_group.description,
        'depth_tier': subject_group.depth_tier,
        'discipline': subject_group.discipline,
        'accent_color': subject_group.accent_color,
        'strands': [{
            'id': s.id,
            'name': s.name,
            'summary': s.summary,
            'topic_count': s.topic_count
        } for s in subject_group.strands]
    })


# ---------------------------------------------------------------------------
# Strand Endpoints
# ---------------------------------------------------------------------------

@curriculum_bp.route('/strands', methods=['GET'])
def get_strands():
    """Get all strands, optionally filtered by subject group."""
    subject_group_id = request.args.get('subject_group_id')
    
    query = Strand.query
    if subject_group_id:
        query = query.filter_by(subject_group_id=subject_group_id)
    
    strands = query.order_by(Strand.sort_order).all()
    
    return jsonify([{
        'id': s.id,
        'programme_id': s.programme_id,
        'subject_group_id': s.subject_group_id,
        'name': s.name,
        'summary': s.summary,
        'spec_ref': s.spec_ref,
        'topic_count': s.topic_count,
        'sort_order': s.sort_order
    } for s in strands])


@curriculum_bp.route('/strands/<string:strand_id>', methods=['GET'])
def get_strand(strand_id):
    """Get details of a specific strand with topics."""
    strand = Strand.query.get_or_404(strand_id)
    
    return jsonify({
        'id': strand.id,
        'programme_id': strand.programme_id,
        'subject_group_id': strand.subject_group_id,
        'name': strand.name,
        'summary': strand.summary,
        'spec_ref': strand.spec_ref,
        'topic_count': strand.topic_count,
        'topics': [{
            'id': t.id,
            'name': t.name,
            'summary': t.summary,
            'depth_tier': t.depth_tier
        } for t in strand.topics]
    })


# ---------------------------------------------------------------------------
# Topic Endpoints
# ---------------------------------------------------------------------------

@curriculum_bp.route('/topics', methods=['GET'])
def get_topics():
    """Get all topics, with optional filters."""
    programme_id = request.args.get('programme_id')
    subject_group_id = request.args.get('subject_group_id')
    strand_id = request.args.get('strand_id')
    search = request.args.get('search')
    
    query = Topic.query
    
    if programme_id:
        query = query.filter_by(programme_id=programme_id)
    if subject_group_id:
        query = query.filter_by(subject_group_id=subject_group_id)
    if strand_id:
        query = query.filter_by(strand_id=strand_id)
    if search:
        query = query.filter(Topic.name.ilike(f'%{search}%'))
    
    topics = query.all()
    
    return jsonify([{
        'id': t.id,
        'programme_id': t.programme_id,
        'subject_group_id': t.subject_group_id,
        'strand_id': t.strand_id,
        'name': t.name,
        'summary': t.summary,
        'depth_tier': t.depth_tier,
        'key_concepts': t.key_concepts_list,
        'vocabulary_count': len(t.vocabulary_list)
    } for t in topics])


@curriculum_bp.route('/topics/<string:topic_id>', methods=['GET'])
def get_topic(topic_id):
    """Get full details of a specific topic."""
    topic = Topic.query.get_or_404(topic_id)
    
    return jsonify({
        'id': topic.id,
        'programme_id': topic.programme_id,
        'subject_group_id': topic.subject_group_id,
        'strand_id': topic.strand_id,
        'name': topic.name,
        'summary': topic.summary,
        'key_concepts': topic.key_concepts_list,
        'related_concepts': json.loads(topic.related_concepts) if topic.related_concepts else [],
        'concepts': json.loads(topic.concepts) if topic.concepts else [],
        'global_context_links': json.loads(topic.global_context_links) if topic.global_context_links else [],
        'atl_links': json.loads(topic.atl_links) if topic.atl_links else [],
        'criteria_focus': json.loads(topic.criteria_focus) if topic.criteria_focus else [],
        'depth_tier': topic.depth_tier,
        'vocabulary': topic.vocabulary_list,
        'learning_objectives': json.loads(topic.learning_objectives) if topic.learning_objectives else {},
        'progression': topic.progression_list,
        'misconceptions': json.loads(topic.misconceptions) if topic.misconceptions else [],
        'skills_graph': json.loads(topic.skills_graph) if topic.skills_graph else {},
        'lesson_engine': json.loads(topic.lesson_engine) if topic.lesson_engine else {},
        'practice_seeds': json.loads(topic.practice_seeds) if topic.practice_seeds else [],
        'newton_prompts': json.loads(topic.newton_prompts) if topic.newton_prompts else [],
        'uoi_links': json.loads(topic.uoi_links) if topic.uoi_links else [],
        'question_count': len(topic.question_bank)
    })


# ---------------------------------------------------------------------------
# Question Bank Endpoints
# ---------------------------------------------------------------------------

@curriculum_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get question bank items, with optional filters."""
    topic_id = request.args.get('topic_id')
    subject_tag = request.args.get('subject_tag')
    difficulty = request.args.get('difficulty')
    question_type = request.args.get('question_type')
    
    query = QuestionBankItem.query
    
    if topic_id:
        query = query.filter_by(topic_id=topic_id)
    if subject_tag:
        query = query.filter_by(subject_tag=subject_tag)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    if question_type:
        query = query.filter_by(question_type=question_type)
    
    questions = query.all()
    
    return jsonify([{
        'id': q.id,
        'topic_id': q.topic_id,
        'question_text': q.question_text,
        'question_type': q.question_type,
        'difficulty_level': q.difficulty_level,
        'options': q.options_list,
        'marks': q.marks,
        'subject_tag': q.subject_tag,
        'tags': json.loads(q.tags) if q.tags else []
    } for q in questions])


@curriculum_bp.route('/questions/<string:question_id>', methods=['GET'])
def get_question(question_id):
    """Get full details of a specific question (for practice)."""
    question = QuestionBankItem.query.get_or_404(question_id)
    
    return jsonify({
        'id': question.id,
        'topic_id': question.topic_id,
        'question_text': question.question_text,
        'question_type': question.question_type,
        'difficulty_level': question.difficulty_level,
        'options': question.options_list,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'hints': question.hints_list,
        'marks': question.marks,
        'subject_tag': question.subject_tag,
        'tags': json.loads(question.tags) if question.tags else []
    })


@curriculum_bp.route('/questions/random', methods=['GET'])
def get_random_questions():
    """Get random questions for practice sessions."""
    topic_id = request.args.get('topic_id')
    count = request.args.get('count', 10, type=int)
    difficulty = request.args.get('difficulty')
    
    query = QuestionBankItem.query
    
    if topic_id:
        query = query.filter_by(topic_id=topic_id)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    
    # Get random questions
    questions = query.order_by(db.func.random()).limit(count).all()
    
    return jsonify([{
        'id': q.id,
        'topic_id': q.topic_id,
        'question_text': q.question_text,
        'question_type': q.question_type,
        'difficulty_level': q.difficulty_level,
        'options': q.options_list,
        'marks': q.marks,
        'subject_tag': q.subject_tag
    } for q in questions])


# Health check
@curriculum_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for curriculum API."""
    return jsonify({'status': 'healthy', 'service': 'curriculum-api'})
"""
Curriculum seeder script - imports Revisions Hub curriculum content into the database.
This script reads JSON curriculum files from the curriculum folder and populates
the database with programmes, subject groups, strands, topics, and question bank items.
"""
import sys
import os
import json
import glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Programme, SubjectGroup, Strand, Topic, QuestionBankItem

# Path to curriculum folder (adjust this path as needed)
CURRICULUM_PATH = "C:/Users/HP/Downloads/revisions-hub-nextjs/curriculum"

def seed_programmes():
    """Seed basic programme data."""
    print("Seeding programmes...")
    
    programmes = [
        {
            "id": "pyp",
            "name": "PYP",
            "full_name": "Primary Years Programme",
            "ages": "3-12",
            "curriculum_model": "IB PYP",
            "programme_meta": json.dumps({"levels": 8, "transdisciplinary": True})
        },
        {
            "id": "myp",
            "name": "MYP",
            "full_name": "Middle Years Programme",
            "ages": "11-16",
            "curriculum_model": "IB MYP",
            "programme_meta": json.dumps({"levels": 5, "subjects": 8})
        },
        {
            "id": "dp",
            "name": "DP",
            "full_name": "Diploma Programme",
            "ages": "16-19",
            "curriculum_model": "IB DP",
            "programme_meta": json.dumps({"levels": 2, "subjects": 6})
        }
    ]
    
    for prog_data in programmes:
        if not Programme.query.filter_by(id=prog_data["id"]).first():
            programme = Programme(**prog_data)
            db.session.add(programme)
            print(f"  [OK] Added programme: {prog_data['name']}")
    
    db.session.commit()

def seed_pyp_curriculum():
    """Seed PYP curriculum from JSON files."""
    print("Seeding PYP curriculum...")
    
    programme = Programme.query.filter_by(id="pyp").first()
    if not programme:
        print("  ✗ PYP programme not found, skipping")
        return
    
    # Define subject groups for PYP
    subject_groups_data = [
        {
            "id": "pyp-math",
            "programme_id": "pyp",
            "slug": "mathematics",
            "name": "Mathematics",
            "kind": "learning_area",
            "description": "Developing number sense, pattern recognition, and mathematical thinking",
            "depth_tier": "full",
            "discipline": "mathematics",
            "accent_color": "#7C3AED",
            "sort_order": 1
        },
        {
            "id": "pyp-sci",
            "programme_id": "pyp",
            "slug": "science",
            "name": "Science",
            "kind": "learning_area",
            "description": "Exploring the natural world through scientific inquiry",
            "depth_tier": "full",
            "discipline": "science",
            "accent_color": "#10B981",
            "sort_order": 2
        },
        {
            "id": "pyp-lang",
            "programme_id": "pyp",
            "slug": "language",
            "name": "Language",
            "kind": "learning_area",
            "description": "Developing communication skills in multiple languages",
            "depth_tier": "full",
            "discipline": "language",
            "accent_color": "#06B6D4",
            "sort_order": 3
        },
        {
            "id": "pyp-soc",
            "programme_id": "pyp",
            "slug": "social-studies",
            "name": "Social Studies",
            "kind": "learning_area",
            "description": "Understanding human societies and their environments",
            "depth_tier": "full",
            "discipline": "social_studies",
            "accent_color": "#F59E0B",
            "sort_order": 4
        },
        {
            "id": "pyp-arts",
            "programme_id": "pyp",
            "slug": "arts",
            "name": "Arts",
            "kind": "learning_area",
            "description": "Creative expression through visual and performing arts",
            "depth_tier": "scaffold",
            "discipline": "arts",
            "accent_color": "#E11D48",
            "sort_order": 5
        },
        {
            "id": "pyp-pspe",
            "programme_id": "pyp",
            "slug": "pspe",
            "name": "PSPE",
            "kind": "learning_area",
            "description": "Personal, Social and Physical Education",
            "depth_tier": "scaffold",
            "discipline": "physical_education",
            "accent_color": "#4F46E5",
            "sort_order": 6
        },
        {
            "id": "pyp-dig",
            "programme_id": "pyp",
            "slug": "digital-literacy",
            "name": "Digital Literacy",
            "kind": "learning_area",
            "description": "Technology and digital skills for the modern world",
            "depth_tier": "scaffold",
            "discipline": "technology",
            "accent_color": "#9333EA",
            "sort_order": 7
        }
    ]
    
    for sg_data in subject_groups_data:
        if not SubjectGroup.query.filter_by(id=sg_data["id"]).first():
            subject_group = SubjectGroup(**sg_data)
            db.session.add(subject_group)
            print(f"  [OK] Added subject group: {sg_data['name']}")
    
    db.session.commit()
    
    # Process curriculum JSON files
    pyp_path = os.path.join(CURRICULUM_PATH, "pyp", "fragments")
    
    for subject_group_id in ["mathematics", "science", "language", "social-studies", "arts", "pspe", "digital-literacy"]:
        subject_path = os.path.join(pyp_path, subject_group_id)
        if not os.path.exists(subject_path):
            print(f"  [WARN] Subject folder not found: {subject_group_id}")
            continue
        
        # Process JSON files in subject folder
        json_files = glob.glob(os.path.join(subject_path, "*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Process strand data
                if "strand" in data:
                    strand_data = data["strand"]
                    strand_id = strand_data["id"]
                    
                    # Find corresponding subject group
                    sg_slug = subject_group_id.replace("-", "")
                    subject_group = SubjectGroup.query.filter_by(
                        programme_id="pyp",
                        slug=sg_slug
                    ).first()
                    
                    if not subject_group:
                        # Try to match by kind
                        subject_group = SubjectGroup.query.filter_by(
                            programme_id="pyp",
                            slug=subject_group_id
                        ).first()
                    
                    if subject_group and not Strand.query.filter_by(id=strand_id).first():
                        strand = Strand(
                            id=strand_id,
                            programme_id="pyp",
                            subject_group_id=subject_group.id,
                            name=strand_data["name"],
                            summary=strand_data.get("summary"),
                            spec_ref=strand_data.get("spec_ref"),
                            topic_count=len(data.get("topics", [])),
                            sort_order=0
                        )
                        db.session.add(strand)
                        print(f"    [OK] Added strand: {strand_data['name']}")
                
                # Process topics
                if "topics" in data:
                    for topic_data in data["topics"]:
                        topic_id = topic_data["id"]
                        
                        if not Topic.query.filter_by(id=topic_id).first():
                            # Find strand
                            strand = Strand.query.filter_by(id=topic_data["strand_id"]).first()
                            if not strand:
                                continue
                            
                            # Find subject group
                            subject_group = SubjectGroup.query.filter_by(id=strand.subject_group_id).first()
                            if not subject_group:
                                continue
                            
                            topic = Topic(
                                id=topic_id,
                                programme_id="pyp",
                                subject_group_id=subject_group.id,
                                strand_id=strand.id,
                                name=topic_data["name"],
                                summary=topic_data.get("summary"),
                                key_concepts=json.dumps(topic_data.get("key_concepts", [])),
                                related_concepts=json.dumps(topic_data.get("related_concepts", [])),
                                concepts=json.dumps(topic_data.get("concepts", [])),
                                vocabulary=json.dumps(topic_data.get("vocabulary", [])),
                                learning_objectives=json.dumps(topic_data.get("learning_objectives", {})),
                                progression=json.dumps(topic_data.get("progression", [])),
                                misconceptions=json.dumps(topic_data.get("misconceptions", [])),
                                skills_graph=json.dumps(topic_data.get("skills_graph", {})),
                                lesson_engine=json.dumps(topic_data.get("lesson_engine", {})),
                                practice_seeds=json.dumps(topic_data.get("practice_seeds", [])),
                                newton_prompts=json.dumps(topic_data.get("newton_prompts", [])),
                                uoi_links=json.dumps(topic_data.get("uoi_links", [])),
                                depth_tier="full"
                            )
                            db.session.add(topic)
                            print(f"      [OK] Added topic: {topic_data['name']}")
                
                db.session.commit()
                
            except Exception as e:
                print(f"    [ERROR] Error processing {json_file}: {e}")
                continue

def seed_sample_questions():
    """Seed sample question bank items."""
    print("Seeding sample question bank items...")
    
    # Get some topics to add questions to
    topics = Topic.query.limit(10).all()
    
    sample_questions = [
        {
            "question_text": "What is the result of 15 + 27?",
            "question_type": "multiple_choice",
            "difficulty_level": "easy",
            "correct_answer": "42",
            "options": json.dumps(["38", "42", "45", "52"]),
            "explanation": "15 + 27 = 42. Add the tens (10 + 20 = 30) and ones (5 + 7 = 12), then combine: 30 + 12 = 42.",
            "hints": json.dumps(["Add the tens first", "Then add the ones"]),
            "marks": 1,
            "subject_tag": "mathematics",
            "tags": json.dumps(["addition", "basic", "calculation"])
        },
        {
            "question_text": "Which of the following is a prime number?",
            "question_type": "multiple_choice",
            "difficulty_level": "medium",
            "correct_answer": "17",
            "options": json.dumps(["15", "17", "21", "27"]),
            "explanation": "A prime number is only divisible by 1 and itself. 17 is only divisible by 1 and 17.",
            "hints": json.dumps(["Check divisibility by small numbers", "Prime numbers have exactly 2 factors"]),
            "marks": 2,
            "subject_tag": "mathematics",
            "tags": json.dumps(["prime", "number_theory", "properties"])
        },
        {
            "question_text": "Explain the concept of one-to-one correspondence in counting.",
            "question_type": "short_answer",
            "difficulty_level": "medium",
            "correct_answer": "One-to-one correspondence means matching one number word to exactly one object being counted.",
            "explanation": "This fundamental counting skill ensures that each object is counted exactly once.",
            "hints": json.dumps(["Think about pointing to objects", "Each object gets one number"]),
            "marks": 3,
            "subject_tag": "mathematics",
            "tags": json.dumps(["counting", "fundamental", "correspondence"])
        }
    ]
    
    for i, topic in enumerate(topics):
        for j, q_data in enumerate(sample_questions):
            question_id = f"q-{topic.id}-{j}"
            if not QuestionBankItem.query.filter_by(id=question_id).first():
                question = QuestionBankItem(
                    id=question_id,
                    topic_id=topic.id,
                    **q_data
                )
                db.session.add(question)
                print(f"  [OK] Added question to topic: {topic.name}")
    
    db.session.commit()

def seed_curriculum():
    """Main function to seed all curriculum data."""
    app = create_app()
    
    with app.app_context():
        print("Starting curriculum seeding for Solemn Scholars...\n")
        
        try:
            seed_programmes()
            seed_pyp_curriculum()
            seed_sample_questions()
            
            print("\n[SUCCESS] Curriculum seeding completed successfully!")
            print(f"\n[SUMMARY]")
            print(f"  - Programmes: {Programme.query.count()}")
            print(f"  - Subject Groups: {SubjectGroup.query.count()}")
            print(f"  - Strands: {Strand.query.count()}")
            print(f"  - Topics: {Topic.query.count()}")
            print(f"  - Question Bank Items: {QuestionBankItem.query.count()}")
            
        except Exception as e:
            print(f"\n[ERROR] Error during curriculum seeding: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    seed_curriculum()
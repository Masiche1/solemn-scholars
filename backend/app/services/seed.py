"""Seed the database with realistic demo data for Tutorly."""
import random
from datetime import datetime, timedelta
from app import db
from app.models import (
    User, TutorProfile, Subject, Location, Availability, Job, Application,
    Conversation, Message, Booking, Review, Lead, SavedTutor,
)

SUBJECTS = [
    # (name, slug, icon, description, tutor_count, rating, price_from, accent)
    ("Mathematics", "mathematics", "\u2797", "Algebra, Geometry, Calculus and problem solving", 1240, 4.9, 8, "blue", "mathematics.jpg", "√x"),
    ("English", "english", "\U0001f4d6", "Improve reading, writing, grammar and communication", 1180, 4.8, 8, "purple", "english.jpg", "Aa"),
    ("Physics", "physics", "\u269b\ufe0f", "Mechanics, Electricity, Thermodynamics and more", 950, 4.9, 9, "navy", "physics.jpg", "⚛"),
    ("Chemistry", "chemistry", "\u2697\ufe0f", "Organic, Inorganic, Physical Chemistry and more", 890, 4.8, 9, "teal", "chemistry.jpg", "⚗"),
    ("Biology", "biology", "\U0001f9ec", "Cell biology, Genetics, Anatomy and more", 860, 4.8, 9, "green", "biology.jpg", "♧"),
    ("Computer Science", "computer-science", "\U0001f4bb", "Data Structures, Algorithms, Databases and more", 1050, 4.9, 10, "blue", "computer-science.jpg", "▣"),
    ("Programming", "programming", "\U0001f468\u200d\U0001f4bb", "Python, Java, C++, JavaScript and more", 1310, 4.9, 10, "purple", "programming.jpg", "</>"),
    ("History", "history", "\U0001f3db\ufe0f", "World, Modern, Ancient history and more", 620, 4.7, 8, "gold", "history.jpg", "⌂"),
    ("Geography", "geography", "\U0001f30d", "Maps, Climate, Earth Science and more", 600, 4.7, 8, "green", "geography.jpg", "◎"),
    ("Business Studies", "business-studies", "\U0001f4ca", "Management, Marketing, Entrepreneurship and more", 780, 4.8, 9, "navy", "business-studies.jpg", "▣"),
    ("Economics", "economics", "\U0001f4c8", "Microeconomics, Macroeconomics, Markets and more", 650, 4.8, 9, "teal", "economics.jpg", "↗"),
    ("Accounting", "accounting", "\U0001f9ee", "Financial Accounting, Bookkeeping, Auditing and more", 710, 4.8, 9, "blue", "accounting.jpg", "▤"),
    ("Languages", "languages", "\U0001f5e3\ufe0f", "Learn new languages and improve fluency", 1300, 4.9, 8, "pink", "languages.jpg", "文"),
    ("French", "french", "\U0001f1eb\U0001f1f7", "Learn French language, grammar and culture", 540, 4.8, 8, "pink", "french.jpg", "A"),
    ("Spanish", "spanish", "\U0001f1ea\U0001f1f8", "Learn Spanish language, grammar and culture", 560, 4.8, 8, "coral", "spanish.jpg", "A"),
    ("Arabic", "arabic", "\U0001f3db\ufe0f", "Learn Arabic language, reading and culture", 460, 4.7, 8, "gold", "arabic.jpg", "ع"),
    ("Music", "music", "\U0001f3b5", "Piano, Guitar, Theory, Composition and more", 680, 4.8, 10, "purple", "music.jpg", "♫"),
    ("Art & Design", "art-design", "\U0001f3a8", "Drawing, Painting, Digital Art, Graphic Design and more", 420, 4.8, 10, "coral", "art-design.jpg", "◉"),
    ("Robotics", "robotics", "\U0001f916", "Robotics, Automation, Electronics and more", 430, 4.8, 10, "blue", "robotics.jpg", "⚙"),
    ("STEM", "stem", "\U0001f52c", "Science, Technology, Engineering, Mathematics", 900, 4.9, 9, "blue", "stem.jpg", "✦"),
    ("IELTS Test Prep", "ielts-test-prep", "\U0001f4dd", "Reading, Writing, Listening, Speaking and more", 850, 4.8, 9, "purple", "ielts.jpg", "✓"),
]

LOCATIONS = ["London", "Manchester", "Birmingham", "Edinburgh", "Bristol", "Leeds", "Online Only"]

TUTORS = [
    {
        "name": "Sarah Mitchell", "headline": "Experienced Maths & Physics Tutor | PGCE Qualified",
        "bio": "I'm a fully qualified maths and physics teacher with over ten years of classroom and one-to-one experience. I specialise in helping GCSE and A-Level students turn anxiety into confidence, breaking complex problems into manageable steps and reinforcing understanding through practice.",
        "approach": "Every learner is different. I start by identifying gaps and learning style, then build a personalised plan that mixes concept explanation, worked examples, and targeted practice. I focus on understanding over memorisation so students can tackle unfamiliar questions with confidence.",
        "qualifications": "PGCE in Secondary Mathematics, University of Cambridge\nBSc Physics, Imperial College London\nEnhanced DBS checked",
        "years": 11, "rate": 45, "modes": "online,in-person", "location": "London",
        "languages": "English, French", "response": "usually within an hour",
        "verification": "verified", "subjects": ["Mathematics", "Physics", "IELTS Test Prep"],
    },
    {
        "name": "James Okoro", "headline": "Software Engineer & Coding Mentor | Python, Web Dev",
        "bio": "I'm a senior software engineer who loves teaching the next generation of developers. Whether you're starting your first line of Python or preparing for a technical interview, I'll meet you where you are and help you build real, portfolio-worthy projects.",
        "approach": "Learning by doing. Each session we build something tangible, from scripts to web apps. I emphasise problem decomposition, clean code, and debugging skills that transfer to any language. I adapt pace to the learner and provide project briefs to keep momentum between sessions.",
        "qualifications": "MSc Computer Science, University of Edinburgh\n5 years industry experience\nGoogle Certified Educator",
        "years": 6, "rate": 55, "modes": "online", "location": "Online Only",
        "languages": "English, Igbo", "response": "within a few hours",
        "verification": "verified", "subjects": ["Programming", "Mathematics"],
    },
    {
        "name": "Emily Chen", "headline": "English & Creative Writing Tutor | 11+ and GCSE Specialist",
        "bio": "I help students find their voice. From 11+ entrance exams to A-Level literature, I tailor sessions to build both technical accuracy and creative confidence. My students have gained places at top grammar and independent schools across the country.",
        "approach": "I combine close reading, structured writing frameworks, and creative play. We analyse model texts, practise timed responses, and develop a personal editing checklist. For younger learners I use games and storytelling to make grammar stick.",
        "qualifications": "BA English Literature, University of Oxford (First Class)\nMA Creative Writing, UEA\nCELTA certified",
        "years": 8, "rate": 40, "modes": "online,in-person", "location": "Manchester",
        "languages": "English, Mandarin", "response": "within a few hours",
        "verification": "verified", "subjects": ["English", "IELTS Test Prep"],
    },
    {
        "name": "Dr. Anita Rao", "headline": "PhD Chemist | Chemistry & Biology from KS3 to Degree Level",
        "bio": "With a doctorate in chemistry and years of tutoring experience, I support students from KS3 science through to undergraduate chemistry. I make abstract concepts tangible with analogies, diagrams, and real-world examples.",
        "approach": "I diagnose misconceptions first, then rebuild understanding with visual models and incremental practice. Sessions include exam-style questions from the start so students feel prepared, not panicked. I provide concise notes after every lesson.",
        "qualifications": "PhD Chemistry, University of Bristol\nBSc Biochemistry, UCL\nFellow of the Royal Society of Chemistry",
        "years": 12, "rate": 60, "modes": "online,in-person", "location": "Bristol",
        "languages": "English, Hindi, Telugu", "response": "within a day",
        "verification": "verified", "subjects": ["Chemistry", "Biology", "STEM", "IELTS Test Prep"],
    },
    {
        "name": "Marcus Bell", "headline": "Languages Tutor | Spanish & French for Travel, Exams, Business",
        "bio": "¡Hola! Bonjour! I'm a multilingual tutor passionate about helping people communicate with confidence. I've lived in Madrid and Paris and bring cultural context into every lesson, from casual conversation to formal exam prep.",
        "approach": "Communicative and immersive. We speak the target language from lesson one, using role-plays, real-world materials, and spaced repetition for vocabulary. Grammar is taught in context, not as dry rules. I set small, achievable goals each week.",
        "qualifications": "BA Modern Languages, University of Leeds\nDELE C2 Spanish\nDALF C2 French\nTEFL certified",
        "years": 9, "rate": 38, "modes": "online,in-person", "location": "Edinburgh",
        "languages": "English, Spanish, French, Italian", "response": "within a few hours",
        "verification": "verified", "subjects": ["Spanish", "French", "Languages"],
    },
    {
        "name": "Priya Sharma", "headline": "Piano & Music Theory Tutor | ABRSM Grade 1–8",
        "bio": "I teach piano and music theory to students of all ages, from complete beginners to grade 8 candidates. My lessons are patient, encouraging, and tailored to each student's musical interests, whether classical, pop, or film scores.",
        "approach": "I blend technique, theory, and repertoire so learning stays musical and motivating. We set goals together—exams, performances, or playing for pleasure—and I provide practice strategies that make progress visible week to week.",
        "qualifications": "MMus Piano Performance, Royal Academy of Music\nLRSM Diploma\nABRSM Certified Teacher",
        "years": 7, "rate": 42, "modes": "in-person,online", "location": "Birmingham",
        "languages": "English, Hindi", "response": "within a few hours",
        "verification": "verified", "subjects": ["Music"],
    },
    {
        "name": "David Thompson", "headline": "History & Economics Tutor | Exam Prep & Essay Skills",
        "bio": "I help students master content and craft compelling essays. Specialising in History and Economics at GCSE and A-Level, I focus on argument, evidence, and exam technique—the skills that move grades from good to outstanding.",
        "approach": "Sessions combine knowledge consolidation with structured essay practice. We use past-paper questions, mark-scheme analysis, and timed writing to build fluency. I give detailed, actionable feedback that targets the next step in improvement.",
        "qualifications": "MA History, University of Cambridge\nBA Economics, LSE\nQualified Teacher Status",
        "years": 10, "rate": 44, "modes": "online", "location": "Online Only",
        "languages": "English", "response": "within a day",
        "verification": "verified", "subjects": ["History", "Economics", "IELTS Test Prep", "English"],
    },
    {
        "name": "Sofia Garcia", "headline": "Early Years & Primary Tutor | Building Confident Learners",
        "bio": "I work with younger learners aged 5–11, building strong foundations in literacy and numeracy through play, stories, and lots of encouragement. I have a particular passion for helping reluctant readers discover the joy of books.",
        "approach": "Learning should feel like an adventure. I use games, manipulatives, and stories to teach core skills, celebrating every small win. I keep parents informed with simple weekly updates and practical ideas to support learning at home.",
        "qualifications": "BA Primary Education, University of Manchester\nPGCE Early Years\nEnhanced DBS checked",
        "years": 5, "rate": 32, "modes": "in-person", "location": "Leeds",
        "languages": "English, Spanish", "response": "within a few hours",
        "verification": "verified", "subjects": ["Mathematics", "English"],
    },
    {
        "name": "Tom Wright", "headline": "Maths Tutor | KS3, GCSE & Functional Skills",
        "bio": "I make maths click. I work with students who feel stuck or anxious about maths, using visual methods and real-life examples to rebuild confidence. I also support adult learners working towards functional skills qualifications.",
        "approach": "I find the gap, then bridge it. Sessions focus on one key idea at a time with plenty of practice and immediate feedback. I celebrate progress and normalise mistakes as part of learning. Every student gets a personalised topic tracker.",
        "qualifications": "BSc Mathematics, University of Sheffield\nPGCE Mathematics\nNCETM Accredited",
        "years": 4, "rate": 30, "modes": "online,in-person", "location": "London",
        "languages": "English", "response": "within a day",
        "verification": "pending", "subjects": ["Mathematics", "IELTS Test Prep"],
    },
    {
        "name": "Hannah Lee", "headline": "University Admissions Coach | Personal Statements & Interviews",
        "bio": "I guide students through the university application process, from choosing courses to crafting standout personal statements and preparing for interviews. I've supported successful applicants to Russell Group universities and Oxbridge.",
        "approach": "I help students tell their own story authentically. We map experiences to course requirements, draft and refine personal statements iteratively, and practise interviews with realistic mock questions and constructive feedback.",
        "qualifications": "MEd University Admissions Counselling, UCL\nBA PPE, University of Oxford",
        "years": 6, "rate": 50, "modes": "online", "location": "Online Only",
        "languages": "English, Korean", "response": "within a few hours",
        "verification": "verified", "subjects": ["English", "IELTS Test Prep"],
    },
]

STUDENTS = [
    {"name": "Alex Johnson", "email": "alex@example.com", "password": "student123"},
    {"name": "Maria Santos", "email": "maria@example.com", "password": "student123"},
]

JOBS = [
    {"title": "Maths tutor needed for GCSE student", "subject": "Mathematics", "level": "GCSE",
     "goals": "Struggling with algebra and ratio; needs to build confidence before summer exams.",
     "mode": "online", "location": "Online", "bmin": 30, "bmax": 45, "schedule": "2 sessions per week, evenings",
     "start": "2025-09-10", "requester": 1},
    {"title": "A-Level Chemistry support for Year 13", "subject": "Chemistry", "level": "A-Level",
     "goals": "Organic chemistry and titration calculations; aiming for A grade.",
     "mode": "either", "location": "Bristol", "bmin": 40, "bmax": 60, "schedule": "Weekly, weekend mornings",
     "start": "2025-09-15", "requester": 2},
    {"title": "11+ English and verbal reasoning", "subject": "English", "level": "11+",
     "goals": "Grammar school entrance preparation; comprehension and creative writing.",
     "mode": "in-person", "location": "Manchester", "bmin": 30, "bmax": 40, "schedule": "1 session per week, Saturday",
     "start": "2025-09-20", "requester": 1},
    {"title": "Beginner Python for a curious teen", "subject": "Programming", "level": "Beginner",
     "goals": "14-year-old wants to learn programming through small projects and games.",
     "mode": "online", "location": "Online", "bmin": 35, "bmax": 50, "schedule": "Flexible, 1-2 sessions per week",
     "start": "2025-09-12", "requester": 2},
    {"title": "Conversational French for adult learner", "subject": "French", "level": "Intermediate",
     "goals": "Improving spoken fluency ahead of a move to Lyon; business context helpful.",
     "mode": "online", "location": "Online", "bmin": 30, "bmax": 45, "schedule": "2 sessions per week, lunchtimes",
     "start": "2025-09-08", "requester": 1},
    {"title": "Piano lessons for 8-year-old beginner", "subject": "Music", "level": "Beginner",
     "goals": "Fun, encouraging first piano experience; keen to learn simple songs.",
     "mode": "in-person", "location": "Birmingham", "bmin": 35, "bmax": 45, "schedule": "Weekly, after school",
     "start": "2025-09-25", "requester": 2},
]

REVIEWS = [
    (4.9, "Sarah completely changed my daughter's attitude to maths. She went from dreading lessons to asking for extra practice. Worth every penny.", "Parent of GCSE student"),
    (5.0, "James is brilliant. We built a weather app together over six weeks and I learned more than in a whole term of school.", "Year 10 student"),
    (4.8, "Emily's feedback on my personal statement was invaluable. She helped me find the thread that tied everything together.", "A-Level student"),
    (5.0, "Dr Rao explains organic chemistry in a way that finally makes sense. My mock grade jumped two levels.", "Year 13 student"),
    (4.9, "Marcus made French fun again. I can actually hold a conversation now and I'm not afraid to make mistakes.", "Adult learner"),
    (4.7, "Priya is patient and kind. My son looks forward to piano every week and practises without being asked.", "Parent"),
    (4.9, "David's essay method is gold. I understand how to build an argument now, not just list facts.", "A-Level History student"),
    (5.0, "Sofia helped my daughter read her first chapter book. The confidence boost has been incredible.", "Parent"),
    (4.8, "Hannah was calm and organised throughout the whole application process. Couldn't have done it without her.", "Oxbridge applicant"),
]


def seed_database():
    """Seed the database if it appears empty."""
    if User.query.first() is not None:
        return

    # Subjects
    subject_objs = {}
    for name, slug, icon, description, tutor_count, rating, price_from, accent, image, symbol in SUBJECTS:
        s = Subject(name=name, slug=slug, icon=icon, description=description,
                    tutor_count=tutor_count, rating=rating, price_from=price_from,
                    accent=accent, image=image, symbol=symbol)
        db.session.add(s)
        subject_objs[name] = s
    db.session.flush()

    # Locations
    location_objs = {}
    for name in LOCATIONS:
        loc = Location(name=name, slug=name.lower().replace(" ", "-"))
        db.session.add(loc)
        location_objs[name] = loc
    db.session.flush()

    # Admin
    admin = User(name="Admin User", email="admin@tutorly.com", role="admin",
                 status="active", avatar_url="https://i.pravatar.cc/200?img=68")
    admin.set_password("admin123")
    db.session.add(admin)

    # Students
    students = []
    for sdata in STUDENTS:
        s = User(name=sdata["name"], email=sdata["email"], role="student", status="active",
                 avatar_url=f"https://i.pravatar.cc/200?u={sdata['email']}")
        s.set_password(sdata["password"])
        db.session.add(s)
        students.append(s)
    db.session.flush()

    # Tutors
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    tutor_profiles = []
    for i, tdata in enumerate(TUTORS):
        u = User(name=tdata["name"], email=tdata["name"].lower().replace(" ", ".").replace(".", "") + str(i) + "@tutorly.com",
                 role="tutor", status="active",
                 avatar_url=f"https://i.pravatar.cc/200?img={i + 5}")
        u.set_password("tutor123")
        db.session.add(u)
        db.session.flush()

        profile = TutorProfile(
            user_id=u.id,
            headline=tdata["headline"],
            biography=tdata["bio"],
            teaching_approach=tdata["approach"],
            qualifications=tdata["qualifications"],
            years_experience=tdata["years"],
            hourly_rate=tdata["rate"],
            teaching_modes=tdata["modes"],
            location_name=tdata["location"],
            languages=tdata["languages"],
            response_time=tdata["response"],
            verification_status=tdata["verification"],
            profile_status="approved",
            completed_lessons=random.randint(40, 950),
            repeat_learner_rate=random.randint(60, 92),
        )
        for sname in tdata["subjects"]:
            if sname in subject_objs:
                profile.subjects.append(subject_objs[sname])
        # availability: pick 4-6 weekdays
        for wd in random.sample(weekdays, random.randint(4, 6)):
            start = random.choice(["09:00", "10:00", "16:00", "17:00", "18:00", "19:00"])
            sh = int(start.split(":")[0])
            avail = Availability(tutor_id=None, weekday=wd, start_time=start,
                                 end_time=f"{sh + 2}:00", timezone="Europe/London", recurring=True)
            profile.availability.append(avail)
        db.session.add(profile)
        tutor_profiles.append(profile)
    db.session.flush()

    # Reviews: attach to tutor profiles with synthetic authors
    for i, (rating, comment, author_label) in enumerate(REVIEWS):
        tp = tutor_profiles[i % len(tutor_profiles)]
        review = Review(
            author_id=students[i % len(students)].id,
            recipient_id=tp.id,
            rating=rating,
            comment=f"{comment} — {author_label}",
            moderation_status="approved",
            created_at=datetime.utcnow() - timedelta(days=random.randint(5, 120)),
        )
        db.session.add(review)
    db.session.flush()

    # Jobs
    jobs = []
    for jdata in JOBS:
        job = Job(
            requester_id=jdata["requester"],
            title=jdata["title"],
            subject=jdata["subject"],
            level=jdata["level"],
            goals=jdata["goals"],
            teaching_mode=jdata["mode"],
            location=jdata["location"],
            budget_min=jdata["bmin"],
            budget_max=jdata["bmax"],
            schedule=jdata["schedule"],
            start_date=jdata["start"],
            status="open",
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
        db.session.add(job)
        jobs.append(job)
    db.session.flush()

    # Applications: a couple of tutors apply to a couple of jobs
    apply_pairs = [(0, 0), (0, 8), (1, 3), (3, 1), (4, 4), (5, 5), (8, 0)]
    for tutor_idx, job_idx in apply_pairs:
        if tutor_idx < len(tutor_profiles) and job_idx < len(jobs):
            tp = tutor_profiles[tutor_idx]
            app = Application(
                job_id=jobs[job_idx].id,
                tutor_id=tp.user_id,
                message="Hi, I'd love to help with this. I have experience with this level and can tailor sessions to your goals. Happy to discuss a trial lesson.",
                proposed_rate=tp.hourly_rate,
                availability_note="Flexible evenings and weekends",
                status="pending",
            )
            db.session.add(app)
    db.session.flush()

    # Bookings + reviews tied to bookings for a couple
    for i in range(3):
        tp = tutor_profiles[i]
        learner = students[i % len(students)]
        booking = Booking(
            learner_id=learner.id,
            tutor_id=tp.user_id,
            subject=tp.subjects[0].name if tp.subjects else "General",
            start_at=datetime.utcnow() - timedelta(days=10 - i),
            end_at=datetime.utcnow() - timedelta(days=10 - i, hours=-1),
            status="completed",
            price=tp.hourly_rate,
            payment_status="paid",
            meeting_url="https://meet.tutorly.com/demo" if "online" in tp.teaching_modes else None,
        )
        db.session.add(booking)
        db.session.flush()
        rev = Review(
            booking_id=booking.id,
            author_id=learner.id,
            recipient_id=tp.id,
            rating=5,
            comment="Excellent session, very clear and encouraging. Highly recommended.",
            moderation_status="approved",
        )
        db.session.add(rev)

    # A conversation between a student and a tutor
    convo = Conversation(participant_a_id=students[0].id, participant_b_id=tutor_profiles[0].user_id)
    db.session.add(convo)
    db.session.flush()
    db.session.add(Message(conversation_id=convo.id, sender_id=students[0].id,
                           recipient_id=tutor_profiles[0].user_id,
                           body="Hi Sarah, my daughter is preparing for GCSE maths and feels quite anxious. Do you have availability on weekday evenings?"))
    db.session.add(Message(conversation_id=convo.id, sender_id=tutor_profiles[0].user_id,
                           recipient_id=students[0].id,
                           body="Hello! I'd be happy to help. I have slots Tuesday and Thursday at 6pm. Would either of those work for an initial session?",
                           created_at=datetime.utcnow() - timedelta(minutes=30)))

    # Leads
    leads = [
        Lead(source_page="home", subject="Mathematics", level="GCSE", location="London",
             teaching_mode="online", budget="$30-45", email="parent1@example.com",
             phone="07700900001", name="Rebecca White", lifecycle_status="new"),
        Lead(source_page="find-a-tutor", subject="Chemistry", level="A-Level", location="Bristol",
             teaching_mode="in-person", budget="$40-60", email="parent2@example.com",
             phone="07700900002", name="Jonathan Pierce", lifecycle_status="contacted"),
        Lead(source_page="post-a-job", subject="Spanish", level="Beginner", location="Online",
             teaching_mode="online", budget="$25-35", email="learner@example.com",
             name="Diane Cooper", lifecycle_status="matched", assigned_to="Admin User"),
    ]
    for l in leads:
        l.created_at = datetime.utcnow() - timedelta(days=random.randint(1, 10))
        db.session.add(l)

    # Saved tutor
    db.session.add(SavedTutor(student_id=students[0].id, tutor_profile_id=tutor_profiles[1].id))

    db.session.commit()
    print(f"Seeded database: {len(tutor_profiles)} tutors, {len(students)} students, {len(jobs)} jobs, {len(leads)} leads.")

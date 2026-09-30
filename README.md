# Solemn Scholars

Unified learning platform combining **Revisions Hub** (intelligent learning diagnostics) and **Tutors Hub** (tutor marketplace).

## Architecture

- **Backend**: Flask + SQLAlchemy (extended from Tutors Hub)
- **Frontend**: Next.js 16 + React 19 + Tailwind CSS 4 (from Revisions Hub)
- **Database**: SQLite (shared database for both platforms)
- **Design System**: Tutors Hub design (Coral accent, Inter font, warm off-white background)

## Dual-Pathway Access

### Pathway 1: Intelligent Learning → Tutor Marketplace
1. Student starts with diagnostic assessments
2. AI identifies learning weaknesses and creates study plans
3. Student practices and gets AI tutor help
4. When stuck, contextual tutor recommendations appear
5. Tutor marketplace becomes need-based, not generic

### Pathway 2: Direct Marketplace Access
- Students can access the full tutor marketplace directly
- Browse tutors by subject, level, location
- Search, filter, and contact tutors independently
- No requirement to complete diagnostics first

## Project Structure

```
solemn-scholars/
├── backend/           # Flask backend with extended APIs
│   ├── app/          # Flask application (extended from Tutors Hub)
│   ├── static/       # CSS, JS, images
│   ├── templates/    # Jinja2 templates
│   └── scripts/      # Utility scripts
├── frontend/         # Next.js frontend
│   └── webapp/      # Next.js application (from Revisions Hub)
├── database/         # Shared SQLite database
└── README.md
```

## Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python start_flask.py
```

### Frontend Setup
```bash
cd frontend/webapp
npm install
npm run dev
```

## Features

### Revisions Hub
- Diagnostic assessments across subjects
- AI-powered learning analytics
- Personalized study plans
- Practice sessions with instant feedback
- AI tutor (Newton) assistance
- Progress tracking and results

### Tutors Hub
- Comprehensive tutor directory
- Search and filter by subject, level, location
- Tutor profiles with reviews and ratings
- Job posting and application system
- In-platform messaging
- Booking and payment management
- Admin dashboard for platform management

### Integration Features
- Unified authentication across both platforms
- Smart tutor recommendations based on learning data
- Seamless navigation between platforms
- Shared user profiles and preferences
- Contextual marketplace suggestions

## Environment Variables

### Backend (.env)
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///../database/tutorly.db
```

### Frontend (.env.local)
```
API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_DEV_AUTH=true
```

## Database Schema

The shared database includes:
- Users (students, tutors, admins)
- Tutor profiles and availability
- Learning progress and diagnostics
- Jobs, applications, and bookings
- Reviews and messaging
- Subjects and locations

## Design System

Based on Tutors Hub design:
- **Primary Color**: Coral (#ff6b4a)
- **Secondary Color**: Navy (#15294b)
- **Background**: Warm off-white (#f4efe6)
- **Font**: Inter (Google Fonts)
- **Components**: Rounded cards, badges, chips, stat cards

## Development

The system supports both independent platform usage and integrated workflows:
- Students can use either platform independently
- Learning data informs marketplace recommendations
- Marketplace remains fully accessible without diagnostics
- AI intelligence enhances but doesn't gate the marketplace

## License

Proprietary - Solemn Scholars

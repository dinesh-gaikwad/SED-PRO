  
# EntreSkill Hub

EntreSkill Hub is a full-stack Django platform for gamified learning, skill assessment, AI-powered mock interviews, and 1:1 mentorship. Students progress through locked levels by scoring 70% on exams. Passing auto-generates PDF certificates and unlocks the next level.

**Core Flow:**
10th Course -> 70% Exam -> Certificate -> Unlock 12th -> Repeat -> Unlock Graduation -> Unlock Interview Module -> 1:1 Mentorship

---

## Features

### Learning System
- 3 gated levels: 10th Foundation, 12th Advanced, Graduation Skills
- Each level has modules, video content, and a 50-question exam
- 70% passing threshold required to unlock next level
- Progress tracking and percentage storage per user per level

### Certificates
- Auto PDF generation with ReportLab when user passes
- Certificates emailed to user via Celery
- Downloadable from dashboard
- Stored in `media/certificates/{level}/`

### AI Mock Interviews
- WebRTC-based live video interview interface
- AI feedback on answers using OpenAI API
- 3 interview types: HR, Technical, Behavioral
- Score calculation and feedback stored per session

### Mentorship
- Browse active mentors with expertise and bio
- Book 1:1 sessions with date and time selection
- Live video sessions using same WebRTC infrastructure
- Session history and notes

### Additional Modules
- Business Ideas: Curated startup ideas with difficulty tags
- Resume Builder: Dynamic template system
- Interview Prep: Question banks by topic
- Dashboard: Central hub for progress, certificates, unlocks

### Admin
- Django admin for managing courses, modules, questions, mentors
- Bulk upload of questions via CSV
- Monitor user progress and exam results

---

## Tech Stack

**Backend:**
- Django 5.0.6
- Django Channels 4.0.0 for WebRTC signaling
- Celery 5.4.0 for async tasks
- PostgreSQL 15
- Redis 7 for cache and broker

**Frontend:**
- Django Templates + HTML5 + CSS3 + Vanilla JS
- WebRTC for peer-to-peer video
- Responsive design for mobile and desktop

**Infrastructure:**
- Gunicorn + Uvicorn for ASGI
- Nginx for static/media serving and reverse proxy
- Docker + Docker Compose for deployment
- ReportLab for PDF generation

**Integrations:**
- OpenAI API for AI interview feedback
- SMTP for email delivery
- Stripe for payments - optional
- Twilio for SMS/WhatsApp - optional

---

## Project Structure
entreskill_hub/
├── config/                 # Django settings, ASGI, root URLs
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/               # Custom user model, auth
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── education/              # Courses, modules, exams
│   ├── models.py
│   ├── views.py
│   ├── tasks.py            # Certificate generation
│   ├── urls.py
│   └── management/commands/
│       └── load_sample_data.py
├── dashboard/              # User progress, certificate download
│   ├── views.py
│   └── urls.py
├── interview/              # AI mock interviews, WebRTC
│   ├── models.py
│   ├── views.py
│   ├── consumers.py        # Channels WebSocket consumer
│   └── urls.py
├── mentorship/             # Mentor booking, sessions
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── business/               # Business ideas, resume builder
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── core/                   # Landing page, about, contact
│   ├── views.py
│   └── urls.py
├── templates/              # HTML templates
├── media/                  # User uploads, certificates, videos
├── static/                 # CSS, JS, images
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── gunicorn_config.py
└── .env.example

---

## Database Models

### accounts.User
Custom user model extending AbstractUser
- Fields: email, first_name, last_name, phone, profile_image
- Progress: tenth_percentage, twelfth_percentage, graduation_percentage
- Completion flags: tenth_completed, twelfth_completed, graduation_completed
- Certificates: FileField for each level
- Method: can_access_level(level) enforces 70% gate
- Method: update_level_percentage(level, score)

### education.Course
- title, level, description, duration_months
- is_active, is_featured

### education.Module
- ForeignKey to Course
- title, content, order

### education.Exam
- OneToOne to Course
- total_questions, passing_percentage default 70.0

### education.Question
- ForeignKey to Exam
- question_text, options A-D, correct_option

### education.UserExamResult
- ForeignKey to User, Exam
- score, passed, completed_at
- Unique together user + exam

### interview.InterviewSession
- ForeignKey to User
- interview_type: hr, technical, behavioral
- status: active, completed
- overall_score

### interview.InterviewQuestion
- interview_type, question_text, correct_answer

### interview.InterviewAnswer
- ForeignKey to Session, Question
- user_answer, feedback, score

### mentorship.Mentor
- name, email, expertise, bio, profile_image
- is_active, hourly_rate

### mentorship.MentorshipSession
- ForeignKey to User as student, ForeignKey to Mentor
- scheduled_at, topic, status, meeting_link, notes

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node not required for backend

### Local Development Setup

1. Clone repository:
```bash
git clone <repo-url>
cd entreskill_hub
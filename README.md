# CampusBoard 🎓
### A Production-Minded Campus Community Web Application

**CampusBoard** is a full-featured, secure, and modern college community web application built with Python and Django. Designed specifically for university campuses, it consolidates academic resources, lost & found recoveries, campus events, administrative announcements, and peer-to-peer student assistance into an accessible, responsive platform.

---

## 🌟 Key Highlights & Architecture

- **Custom Student Model**: Extends `AbstractUser` using email authentication (no usernames) with college email domain validation (`@college.edu`). Verified students display a campus trust badge.
- **Five Dedicated Categories**:
  - 📚 **Notes & Resources**: Course materials, study summaries, and PDFs.
  - 🔎 **Lost & Found**: Item reporting (lost/found), date, campus location, and resolution tracking.
  - 🎟️ **Events**: Campus workshops, club showcases, dates, start times, and venue locations.
  - 📢 **Announcements**: Campus-wide notices and administrative bulletins.
  - 🤝 **Student Help**: Study groups, capstone recruitment, and peer tutoring.
- **Complete CRUD & Authorization**: Authors manage their own posts (edit/delete) with strict permission checks; unauthenticated users can browse public posts.
- **Search & Filtering**: Live search by query string, category dropdown filtering, status filtering (`active`, `resolved`, `closed`), and chronological sorting.
- **Moderation Workflow**: One-click reporting with duplicate report prevention (`unique_together = ['post', 'reporter']`) and dedicated staff moderation dashboard (`/panel/`).
- **Design System**: Fully bespoke CSS design system inspired by modern design standards (Indigo palette `#4F46E5`, warm neutral surfaces `#F7F8FC`, Inter typography, responsive mobile hamburger drawer, accessible keyboard navigation, and ARIA labels).
- **Automated Test Suite**: 21 unit & integration tests covering authentication, domain enforcement, post CRUD, category validations, search/filter, and moderation.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.14+, Django 6.1 |
| **Database** | SQLite (development) / PostgreSQL (production-ready) |
| **File Handling** | Pillow 12.3.0 (with max 10MB file and format validation) |
| **Frontend** | Semantic HTML5, Vanilla CSS3 (Custom Design Tokens), Vanilla JS |
| **Testing** | Django Test Framework (`django.test.TestCase`) |

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Navigate to the Project Directory
```powershell
cd d:\PYTHON\project_python\campusboard
```

### 3. Apply Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed the Database with Realistic Campus Data
A custom management command is provided to instantly populate the application with realistic campus data:
```powershell
python manage.py seed_data
```
This populates:
- **1 Admin user** (`admin@college.edu` / `AdminPass123!`)
- **5 Student users** (`maya@college.edu`, `alex@college.edu`, etc. / `Pass123!`)
- **14 Posts** across all five categories with various statuses
- **1 Sample Moderation Flag** for demonstration in the admin panel

### 5. Run the Local Development Server
```powershell
python manage.py runserver
```
Open your browser and navigate to:
**http://127.0.0.1:8000/**

---

## 🧪 Running Automated Tests

To run the complete test suite:
```powershell
python manage.py test
```

### Test Coverage Summary:
- **Registration & Auth**: Valid college domain validation, invalid email rejection (`@gmail.com`), password mismatch checks, login, logout, and profile updates.
- **Category-Specific Post Creation**: Validates required fields for each category (e.g., event date for events, lost/found type for lost items).
- **Authorization Enforcement**: Unauthenticated redirects, 403 Forbidden for non-authors attempting to edit/delete other students' posts, author delete/edit success.
- **Search & Filters**: Search term queries against title & description, category filtering, status filtering.
- **Moderation**: Report submission, self-report prevention, duplicate report blocking, staff admin panel access, post removal, and report dismissal.

---

## 🔑 Demo Credentials

| Role | Email | Password | Access Level |
|---|---|---|---|
| **Staff Admin** | `admin@college.edu` | `AdminPass123!` | Moderation Dashboard (`/panel/`), Django Admin (`/admin/`), Full Post Deletion |
| **Student** | `maya@college.edu` | `Pass123!` | Post Creation, Edit/Delete Own Posts, Reporting |
| **Student** | `alex@college.edu` | `Pass123!` | Post Creation, Edit/Delete Own Posts, Reporting |

*New registrations are permitted using any `@college.edu` address.*

---

## 📁 Project Structure

```
campusboard/
├── accounts/                     # User management & authentication app
│   ├── forms.py                  # Student registration, login, profile forms
│   ├── models.py                 # Student custom user model (email auth)
│   ├── tests.py                  # Auth & registration unit tests
│   ├── urls.py                   # /accounts/ routes
│   └── views.py                  # Register, login, logout, profile views
├── posts/                        # Core campus posts & moderation app
│   ├── forms.py                  # Post create/edit and report forms
│   ├── management/commands/      # Custom management commands
│   │   └── seed_data.py          # CampusBoard demo data seeder
│   ├── models.py                 # Post and Report models
│   ├── tests.py                  # Post CRUD, validation, moderation tests
│   ├── urls.py                   # /posts/ routes
│   └── views.py                  # Browse, detail, create, edit, delete, report views
├── campusboard/                  # Project configuration
│   ├── settings.py               # Django settings, domain constraints, file limits
│   ├── urls.py                   # Root URL configuration + custom admin panel routes
│   └── wsgi.py                   # WSGI application entry
├── static/
│   ├── css/style.css             # Comprehensive bespoke design system
│   └── js/main.js                # Vanilla JS for navbar, alerts, conditional form fields
└── templates/
    ├── 404.html                  # Accessible 404 error page
    ├── 500.html                  # Accessible 500 server error page
    ├── base.html                 # Master layout with responsive nav & footer
    ├── home.html                 # Hero, category cards, recent campus activity
    ├── accounts/                 # Login, register, profile templates
    ├── admin_panel/              # Moderation dashboard & confirm delete
    └── posts/                    # Browse, detail, create, edit, delete, my-posts, report
```

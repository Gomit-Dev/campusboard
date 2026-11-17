import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from posts.models import Post, Report

Student = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with realistic campus data across all categories, multiple students, and reports.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding CampusBoard database...'))

        # ── 1. Create Admin and Students ──
        admin, _ = Student.objects.get_or_create(
            email='admin@college.edu',
            defaults={
                'full_name': 'Campus Admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
            }
        )
        admin.set_password('AdminPass123!')
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_verified = True
        admin.save()

        students_data = [
            ('maya@college.edu', 'Maya Patel', 'Pass123!'),
            ('alex@college.edu', 'Alex Rivera', 'Pass123!'),
            ('jordan@college.edu', 'Jordan Lee', 'Pass123!'),
            ('sam@college.edu', 'Samantha Hayes', 'Pass123!'),
            ('liam@college.edu', 'Liam Chen', 'Pass123!'),
        ]

        students = []
        for email, full_name, pwd in students_data:
            s, created = Student.objects.get_or_create(
                email=email,
                defaults={'full_name': full_name, 'is_verified': True}
            )
            s.set_password(pwd)
            s.full_name = full_name
            s.is_verified = True
            s.save()
            students.append(s)

        # ── 2. Create Sample Posts across all 5 Categories ──
        today = datetime.date.today()

        sample_posts = [
            # 📚 Notes & Resources
            {
                'author': students[0],
                'category': 'notes',
                'title': 'CS 301 Data Structures & Algorithms — Complete Exam Review Sheets',
                'description': 'Handwritten and LaTeX summary sheets covering Trees (AVL, Red-Black), Heaps, Graph traversals (BFS/DFS), Dijkstra, and dynamic programming patterns. Verified against Prof. Henderson\'s midterm curriculum.',
                'status': 'active',
            },
            {
                'author': students[1],
                'category': 'notes',
                'title': 'Organic Chemistry II — Reaction Mechanisms Cheatsheet',
                'description': '10-page visual diagram summarizing electrophilic aromatic substitution, carbonyl additions, enolates, and Diels-Alder reactions. Colored arrows show electron flow.',
                'status': 'active',
            },
            {
                'author': students[2],
                'category': 'notes',
                'title': 'PHYS 212 Electromagnetism — Problem Set 4 Solutions Guide',
                'description': 'Step-by-step breakdown of Gauss\'s Law applications, electric flux calculations, and capacitor circuits with explanatory side notes.',
                'status': 'active',
            },

            # 🔎 Lost & Found
            {
                'author': students[3],
                'category': 'lost_found',
                'title': 'Found: Apple AirPods Pro in White Charging Case',
                'description': 'Found sitting on desk #14 in the Science & Engineering Library quiet study floor on level 3. Has a small teal silicone strap attached. Turned in to the circulation desk.',
                'status': 'active',
                'lost_found_type': 'found',
                'item_location': 'Science & Engineering Library (3rd Floor Desk #14)',
                'item_date': today - datetime.timedelta(days=1),
            },
            {
                'author': students[4],
                'category': 'lost_found',
                'title': 'Lost: Navy Blue North Face Backpack with Laptop',
                'description': 'Left behind in Anderson Hall lecture room 102 after Tuesday afternoon chemistry lab. Contains an HP Spectre laptop, lab notebook, and student ID card. Reward offered for safe return!',
                'status': 'active',
                'lost_found_type': 'lost',
                'item_location': 'Anderson Hall Room 102',
                'item_date': today - datetime.timedelta(days=2),
            },
            {
                'author': students[0],
                'category': 'lost_found',
                'title': 'Found: Silver TI-84 Plus CE Graphing Calculator',
                'description': 'Found near the vending machines in the Student Union basement. Has a solar system sticker on the back cover. Claimed and returned to owner!',
                'status': 'resolved',
                'lost_found_type': 'found',
                'item_location': 'Student Union Basement',
                'item_date': today - datetime.timedelta(days=5),
            },

            # 🎟️ Events
            {
                'author': students[1],
                'category': 'events',
                'title': 'Annual Campus Hackathon — HackCampus 2026',
                'description': '36-hour hackathon open to all undergraduate and graduate students! Categories include AI/ML, Sustainability Tech, and Campus Life improvements. Free meals, swag, and $5,000 in prizes. Beginner tracks available.',
                'status': 'active',
                'event_date': today + datetime.timedelta(days=14),
                'event_time': datetime.time(9, 0),
                'event_location': 'Student Innovation Hub, Great Hall',
            },
            {
                'author': students[2],
                'category': 'events',
                'title': 'Graduate School & Research Career Panel',
                'description': 'Featuring faculty advisors and alumni discussing GRE prep, funding opportunities, research fellowships, and balancing industry vs. academia.',
                'status': 'active',
                'event_date': today + datetime.timedelta(days=5),
                'event_time': datetime.time(17, 30),
                'event_location': 'Auditorium C & Zoom Hybrid',
            },
            {
                'author': students[3],
                'category': 'events',
                'title': 'Campus Robotics Club Showcase & Live Demos',
                'description': 'Come check out student-built battlebots, autonomous drones, and line-following rovers. Live demonstrations and club recruitment for new members.',
                'status': 'active',
                'event_date': today + datetime.timedelta(days=8),
                'event_time': datetime.time(14, 0),
                'event_location': 'Engineering Quad Green',
            },

            # 📢 Announcements
            {
                'author': admin,
                'category': 'announcements',
                'title': 'Campus Dining Services & Library Extended Hours for Finals Week',
                'description': 'Starting next Monday, the Main University Library will operate on a 24-hour schedule. Late-night dining options will be available at the Campus Center until 2:00 AM daily with student ID.',
                'status': 'active',
            },
            {
                'author': admin,
                'category': 'announcements',
                'title': 'Spring Semester Course Registration Timelines & Advisor Holds',
                'description': 'Registration windows open by class standing starting October 20th. Please verify that all academic advisor holds and financial check-in items are cleared in your student portal beforehand.',
                'status': 'active',
            },

            # 🤝 Student Help
            {
                'author': students[4],
                'category': 'student_help',
                'title': 'Need Full-Stack Developer for Capstone Project (React / Django)',
                'description': 'Our 3-person team is looking for a fourth member skilled in backend APIs or React frontend for an AI-powered smart irrigation capstone. Meets Tuesdays and Thursdays.',
                'status': 'active',
            },
            {
                'author': students[0],
                'category': 'student_help',
                'title': 'Calculus Peer Tutoring Sessions Available (Free)',
                'description': 'Offering free weekly tutoring for Calc 1 & Calc 2 students struggling with integration techniques and series tests. Sunday afternoons at the Student Learning Center.',
                'status': 'active',
            },
        ]

        created_posts = []
        for post_data in sample_posts:
            post, _ = Post.objects.get_or_create(
                title=post_data['title'],
                defaults=post_data,
            )
            created_posts.append(post)

        # ── 3. Create Sample Report for Moderation Demo ──
        spam_post, _ = Post.objects.get_or_create(
            title='Suspicious Off-Campus Housing Ad (Suspicious Link)',
            defaults={
                'author': students[1],
                'category': 'announcements',
                'description': 'Luxury 1-bedroom apartments for only $200/month near campus! Wire deposit today at this external link to secure your spot.',
                'status': 'active',
            }
        )

        Report.objects.get_or_create(
            post=spam_post,
            reporter=students[2],
            defaults={
                'reason': 'fake',
                'details': 'Suspicious rental rate and suspicious external wire transfer link.',
            }
        )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded:\n'
            f'- 1 Admin user (email: admin@college.edu, password: AdminPass123!)\n'
            f'- {len(students)} Student users (password: Pass123!)\n'
            f'- {Post.objects.count()} Posts across all 5 categories\n'
            f'- {Report.objects.count()} Moderation report for testing'
        ))

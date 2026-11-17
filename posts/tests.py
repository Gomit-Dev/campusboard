import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Report

Student = get_user_model()


class PostModelAndCRUDTests(TestCase):
    """Test post creation for each category, authorization, and moderation."""

    def setUp(self):
        self.client = Client()
        self.user1 = Student.objects.create_user(
            email='alice@lpu.in',
            password='Password123!',
            full_name='Alice Smith',
        )
        self.user2 = Student.objects.create_user(
            email='bob@lpu.in',
            password='Password123!',
            full_name='Bob Jones',
        )
        self.admin = Student.objects.create_superuser(
            email='admin@lpu.in',
            password='AdminPassword123!',
            full_name='Admin Staff',
        )

    # ── Category Post Creation ──
    def test_create_notes_post(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:create'), {
            'category': 'notes',
            'title': 'CS101 Algorithms Summary Notes',
            'description': 'Comprehensive notes on sorting, search, and trees.',
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title='CS101 Algorithms Summary Notes')
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.category, 'notes')
        self.assertEqual(post.status, 'active')

    def test_create_events_post_with_date(self):
        self.client.force_login(self.user1)
        event_date = datetime.date.today() + datetime.timedelta(days=7)
        response = self.client.post(reverse('posts:create'), {
            'category': 'events',
            'title': 'Campus Hackathon 2026',
            'description': 'Join us for a 24-hour coding challenge!',
            'event_date': event_date.strftime('%Y-%m-%d'),
            'event_location': 'Tech Hub Hall B',
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title='Campus Hackathon 2026')
        self.assertEqual(post.event_location, 'Tech Hub Hall B')
        self.assertEqual(post.event_date, event_date)

    def test_create_events_post_missing_date_fails(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:create'), {
            'category': 'events',
            'title': 'Invalid Event without Date',
            'description': 'This should fail validation.',
            'event_date': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title='Invalid Event without Date').exists())
        self.assertContains(response, 'Please provide the event date.')

    def test_create_lost_found_post(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:create'), {
            'category': 'lost_found',
            'title': 'Found Blue Hydro Flask',
            'description': 'Left on the 3rd floor library desk near window.',
            'lost_found_type': 'found',
            'item_location': 'Library Floor 3',
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title='Found Blue Hydro Flask')
        self.assertEqual(post.lost_found_type, 'found')
        self.assertEqual(post.item_location, 'Library Floor 3')

    def test_create_lost_found_missing_type_fails(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:create'), {
            'category': 'lost_found',
            'title': 'Item without Lost/Found indicator',
            'description': 'Missing type field.',
            'lost_found_type': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(title='Item without Lost/Found indicator').exists())
        self.assertContains(response, 'Please specify whether the item was lost or found.')

    def test_create_announcements_and_help_posts(self):
        self.client.force_login(self.user1)
        # Announcement
        res_announcement = self.client.post(reverse('posts:create'), {
            'category': 'announcements',
            'title': 'Library Extended Hours During Finals',
            'description': 'Open 24/7 during exam week.',
        })
        self.assertEqual(res_announcement.status_code, 302)
        self.assertTrue(Post.objects.filter(category='announcements').exists())

        # Student Help
        res_help = self.client.post(reverse('posts:create'), {
            'category': 'student_help',
            'title': 'Looking for Study Group: Linear Algebra',
            'description': 'Anyone preparing for Midterm 2 want to team up?',
        })
        self.assertEqual(res_help.status_code, 302)
        self.assertTrue(Post.objects.filter(category='student_help').exists())

    # ── Authorization Checks ──
    def test_unauthenticated_user_cannot_create_post(self):
        response = self.client.post(reverse('posts:create'), {
            'category': 'notes',
            'title': 'Unauthorized Note',
            'description': 'Should redirect to login.',
        })
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_non_author_cannot_edit_post(self):
        post = Post.objects.create(
            author=self.user1,
            category='notes',
            title="Alice's Post",
            description='Original text',
        )
        self.client.force_login(self.user2)
        response = self.client.post(reverse('posts:edit', kwargs={'pk': post.pk}), {
            'category': 'notes',
            'title': 'Hacked Title',
            'description': 'Hacked text',
            'status': 'active',
        })
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
        post.refresh_from_db()
        self.assertEqual(post.title, "Alice's Post")

    def test_non_author_cannot_delete_post(self):
        post = Post.objects.create(
            author=self.user1,
            category='notes',
            title="Alice's Post to Delete",
            description='Original text',
        )
        self.client.force_login(self.user2)
        response = self.client.post(reverse('posts:delete', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_author_can_edit_and_delete_own_post(self):
        post = Post.objects.create(
            author=self.user1,
            category='notes',
            title='My Original Post',
            description='Original text',
        )
        self.client.force_login(self.user1)

        # Edit
        edit_res = self.client.post(reverse('posts:edit', kwargs={'pk': post.pk}), {
            'category': 'notes',
            'title': 'My Updated Post',
            'description': 'Updated text',
            'status': 'resolved',
        })
        self.assertEqual(edit_res.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, 'My Updated Post')
        self.assertEqual(post.status, 'resolved')

        # Delete
        delete_res = self.client.post(reverse('posts:delete', kwargs={'pk': post.pk}))
        self.assertEqual(delete_res.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    # ── Search & Filter ──
    def test_search_and_filtering(self):
        post_math = Post.objects.create(
            author=self.user1,
            category='notes',
            title='Calculus II Study Guide',
            description='Integrals and series practice problems.',
        )
        post_lost = Post.objects.create(
            author=self.user2,
            category='lost_found',
            title='Lost Silver MacBook Charger',
            description='Left in science building room 104.',
            lost_found_type='lost',
        )

        # Search query matching "Calculus"
        res_search = self.client.get(reverse('posts:browse') + '?q=Calculus')
        self.assertContains(res_search, 'Calculus II Study Guide')
        self.assertNotContains(res_search, 'MacBook Charger')

        # Category filter for 'lost_found'
        res_cat = self.client.get(reverse('posts:browse') + '?category=lost_found')
        self.assertContains(res_cat, 'Lost Silver MacBook Charger')
        self.assertNotContains(res_cat, 'Calculus II Study Guide')

    # ── Moderation & Reporting ──
    def test_report_post_submission_and_duplicate_prevention(self):
        post = Post.objects.create(
            author=self.user1,
            category='announcements',
            title='Spam Announcement Post',
            description='Buy cheap crypto here!',
        )
        self.client.force_login(self.user2)

        # First report
        res_report = self.client.post(reverse('posts:report', kwargs={'pk': post.pk}), {
            'reason': 'spam',
            'details': 'Obvious commercial spam.',
        })
        self.assertEqual(res_report.status_code, 302)
        self.assertEqual(Report.objects.filter(post=post).count(), 1)

        # Second report by same user should be blocked
        res_dup = self.client.post(reverse('posts:report', kwargs={'pk': post.pk}), {
            'reason': 'spam',
            'details': 'Reporting again.',
        })
        self.assertEqual(res_dup.status_code, 302)
        self.assertEqual(Report.objects.filter(post=post).count(), 1)

    def test_user_cannot_report_own_post(self):
        post = Post.objects.create(
            author=self.user1,
            category='notes',
            title='Own Note',
            description='Self note',
        )
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:report', kwargs={'pk': post.pk}), {
            'reason': 'spam',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.filter(post=post).count(), 0)

    def test_admin_panel_access_and_moderation_actions(self):
        post = Post.objects.create(
            author=self.user1,
            category='notes',
            title='Post Under Review',
            description='Needs moderation',
        )
        report = Report.objects.create(
            post=post,
            reporter=self.user2,
            reason='inappropriate',
            details='Offensive language',
        )

        # Non-staff user cannot access admin panel
        self.client.force_login(self.user1)
        res_user = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_user.status_code, 302)  # redirects to admin login

        # Staff user can access admin panel
        self.client.force_login(self.admin)
        res_admin = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, 'Post Under Review')

        # Admin dismisses report
        res_dismiss = self.client.post(reverse('admin_dismiss_report', kwargs={'pk': report.pk}))
        self.assertEqual(res_dismiss.status_code, 302)
        self.assertFalse(Report.objects.filter(pk=report.pk).exists())

        # Admin removes post
        res_del = self.client.post(reverse('admin_delete_post', kwargs={'pk': post.pk}))
        self.assertEqual(res_del.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

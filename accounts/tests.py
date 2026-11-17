from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

Student = get_user_model()


class StudentModelTests(TestCase):
    """Test custom Student user model and domain validation."""

    def test_create_student_with_valid_domain(self):
        student = Student.objects.create_user(
            email='alice@lpu.in',
            password='SecretPassword123!',
            full_name='Alice Walker',
        )
        self.assertEqual(student.email, 'alice@lpu.in')
        self.assertEqual(student.full_name, 'Alice Walker')
        self.assertTrue(student.is_verified)
        self.assertTrue(student.check_password('SecretPassword123!'))
        self.assertEqual(student.get_short_name(), 'Alice')
        self.assertEqual(str(student), 'Alice Walker')

    def test_create_superuser(self):
        admin = Student.objects.create_superuser(
            email='admin@lpu.in',
            password='AdminPassword123!',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class StudentAuthTests(TestCase):
    """Test registration, login, logout, and profile flows."""

    def setUp(self):
        self.client = Client()

    def test_registration_with_valid_email_domain(self):
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Bob Miller',
            'email': 'bob@lpu.in',
            'password1': 'ValidPass123!',
            'password2': 'ValidPass123!',
        })
        # Should redirect to home upon successful registration
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Student.objects.filter(email='bob@lpu.in').exists())

    def test_registration_with_invalid_email_domain(self):
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Hacker Dave',
            'email': 'dave@gmail.com',
            'password1': 'ValidPass123!',
            'password2': 'ValidPass123!',
        })
        # Form should be re-rendered with validation error
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(email='dave@gmail.com').exists())
        self.assertContains(response, 'college email address')

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Charlie Puth',
            'email': 'charlie@lpu.in',
            'password1': 'ValidPass123!',
            'password2': 'DifferentPass456!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(email='charlie@lpu.in').exists())

    def test_login_and_logout(self):
        student = Student.objects.create_user(
            email='dan@lpu.in',
            password='TestPassword123!',
            full_name='Dan Brown',
        )

        # Login
        login_res = self.client.post(reverse('accounts:login'), {
            'username': 'dan@lpu.in',
            'password': 'TestPassword123!',
        })
        self.assertRedirects(login_res, reverse('home'))

        # Logout
        logout_res = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(logout_res, reverse('accounts:login'))

    def test_profile_update(self):
        student = Student.objects.create_user(
            email='eva@lpu.in',
            password='TestPassword123!',
            full_name='Eva Green',
        )
        self.client.force_login(student)

        response = self.client.post(reverse('accounts:profile'), {
            'full_name': 'Eva Mendes',
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        student.refresh_from_db()
        self.assertEqual(student.full_name, 'Eva Mendes')

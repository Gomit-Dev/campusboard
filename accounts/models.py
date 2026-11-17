from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class StudentManager(BaseUserManager):
    """Custom manager for Student model that uses email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        
        # Auto-verify if email domain matches campus domain
        from django.conf import settings
        domain = getattr(settings, 'ALLOWED_EMAIL_DOMAIN', 'lpu.in')
        if domain and email.endswith(f'@{domain}'):
            extra_fields.setdefault('is_verified', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', Student.ROLE_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Student(AbstractUser):
    """
    Custom user model for CampusBoard.
    Supports three roles: Student, Teacher, and Admin.
    Uses email as the primary login field instead of username.
    """
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_ADMIN, 'Admin'),
    ]

    # Remove the default username field
    username = None

    email = models.EmailField('college email', unique=True)
    full_name = models.CharField('full name', max_length=150)
    role = models.CharField(
        'role',
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        help_text='Campus role: Student, Teacher, or Admin.',
    )
    is_verified = models.BooleanField(
        'campus member',
        default=False,
        help_text='Indicates whether the user registered with a valid campus email domain.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = StudentManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        role_label = self.get_role_display()
        name = self.full_name or self.email
        return f"{name} ({role_label})"

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email

    @property
    def is_teacher(self):
        return self.role in (self.ROLE_TEACHER, self.ROLE_ADMIN) or self.is_superuser or self.is_staff

    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT and not self.is_teacher and not self.is_admin

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser or self.is_staff

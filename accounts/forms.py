import re

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

Student = get_user_model()


class StudentRegistrationForm(forms.ModelForm):
    """Registration form with student/teacher role selection and email validation."""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = Student
        fields = ['full_name', 'role', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'role': forms.Select(attrs={
                'id': 'id_role',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': f'12345678@{settings.ALLOWED_EMAIL_DOMAIN}',
                'autocomplete': 'email',
                'id': 'id_email',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        # Role-based email validation
        email = cleaned_data.get('email', '').lower().strip()
        role = cleaned_data.get('role') or self.data.get('role') or Student.ROLE_STUDENT
        domain = settings.ALLOWED_EMAIL_DOMAIN
        bypass = getattr(settings, 'BYPASS_EMAIL_DOMAIN_IN_DEBUG', False)

        if email and domain and not (settings.DEBUG and bypass):
            if not email.endswith(f'@{domain}'):
                self.add_error(
                    'email',
                    f'Please use your college email address (@{domain}). Only @{domain} emails are allowed.'
                )
            elif role == Student.ROLE_STUDENT:
                local_part = email.split('@')[0]
                if not re.fullmatch(r'\d{8}', local_part):
                    self.add_error(
                        'email',
                        f'Student email must be your 8-digit registration number followed by @{domain} '
                        f'(e.g. 12345678@{domain}).'
                    )
            elif role == Student.ROLE_TEACHER:
                local_part = email.split('@')[0]
                if not re.fullmatch(r'\d{5}', local_part):
                    self.add_error(
                        'email',
                        f'Teacher email must be your 5-digit employee ID followed by @{domain} '
                        f'(e.g. 12345@{domain}).'
                    )
            elif role == Student.ROLE_ADMIN:
                # Admins must have an email ending in @domain
                pass

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data['password1'])
        role = self.cleaned_data.get('role', Student.ROLE_STUDENT)
        student.role = role

        if role == Student.ROLE_ADMIN:
            student.is_staff = True
            student.is_superuser = True
            student.is_verified = True
        else:
            # Mark as verified if email domain matches
            domain = settings.ALLOWED_EMAIL_DOMAIN
            if domain and student.email.endswith(f'@{domain}'):
                student.is_verified = True
            elif not domain:
                student.is_verified = True
            else:
                student.is_verified = False

        if commit:
            student.save()
        return student


class StudentLoginForm(AuthenticationForm):
    """Login form styled for CampusBoard."""

    username = forms.EmailField(
        label='College Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@lpu.in',
            'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'autocomplete': 'current-password',
        }),
    )


class ProfileUpdateForm(forms.ModelForm):
    """Allow students to update their display name."""

    class Meta:
        model = Student
        fields = ['full_name']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
            }),
        }

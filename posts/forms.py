import os

from django import forms
from django.conf import settings

from .models import Post, Report


class PostForm(forms.ModelForm):
    """Form for creating and editing posts with file validation."""

    class Meta:
        model = Post
        fields = [
            'category', 'title', 'description', 'image', 'file', 'status',
            # Lost & Found fields
            'lost_found_type', 'item_location', 'item_date',
            # Event fields
            'event_date', 'event_time', 'event_location',
        ]
        widgets = {
            'category': forms.Select(attrs={'id': 'id_category'}),
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your post a clear title',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe in detail...',
                'rows': 5,
            }),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'file': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.doc,.docx',
            }),
            'status': forms.Select(),
            # Lost & Found
            'lost_found_type': forms.Select(),
            'item_location': forms.TextInput(attrs={
                'placeholder': 'e.g., Library 2nd floor',
            }),
            'item_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            # Events
            'event_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'event_time': forms.TimeInput(attrs={
                'type': 'time',
            }),
            'event_location': forms.TextInput(attrs={
                'placeholder': 'e.g., Main Auditorium',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        # Restrict 'announcements' category to teachers/staff only
        is_teacher = user and getattr(user, 'is_teacher', False)
        if not is_teacher:
            self.fields['category'].choices = [
                (val, label) for val, label in Post.CATEGORY_CHOICES
                if val != 'announcements'
            ]

        # Make category-specific fields not required at the form level
        # (they'll be validated contextually in clean())
        optional_fields = [
            'lost_found_type', 'item_location', 'item_date',
            'event_date', 'event_time', 'event_location',
            'image', 'file', 'status',
        ]
        for field_name in optional_fields:
            self.fields[field_name].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'name'):
            # Validate extension
            ext = os.path.splitext(image.name)[1].lower()
            allowed = settings.ALLOWED_IMAGE_EXTENSIONS
            if ext not in allowed:
                raise forms.ValidationError(
                    f'Unsupported image format. Allowed: {", ".join(allowed)}'
                )
            # Validate size (10 MB)
            if image.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                max_mb = settings.FILE_UPLOAD_MAX_MEMORY_SIZE // (1024 * 1024)
                raise forms.ValidationError(f'Image must be smaller than {max_mb} MB.')
        return image

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and hasattr(file, 'name'):
            # Validate extension
            ext = os.path.splitext(file.name)[1].lower()
            allowed = settings.ALLOWED_DOCUMENT_EXTENSIONS
            if ext not in allowed:
                raise forms.ValidationError(
                    f'Unsupported file format. Allowed: {", ".join(allowed)}'
                )
            # Validate size (10 MB)
            if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                max_mb = settings.FILE_UPLOAD_MAX_MEMORY_SIZE // (1024 * 1024)
                raise forms.ValidationError(f'File must be smaller than {max_mb} MB.')
        return file

    def clean(self):
        """Category-specific validation — enforce required fields server-side."""
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        # Role-based restriction: only teachers can post announcements
        if category == 'announcements':
            is_teacher = self.user and getattr(self.user, 'is_teacher', False)
            if not is_teacher:
                self.add_error('category', 'Only teachers are authorized to publish announcements.')

        if category == 'lost_found':
            if not cleaned_data.get('lost_found_type'):
                self.add_error('lost_found_type', 'Please specify whether the item was lost or found.')

        if category == 'events':
            if not cleaned_data.get('event_date'):
                self.add_error('event_date', 'Please provide the event date.')

        return cleaned_data


class ReportForm(forms.ModelForm):
    """Form for reporting a post."""

    class Meta:
        model = Report
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(),
            'details': forms.Textarea(attrs={
                'placeholder': 'Provide additional details (optional)',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['details'].required = False

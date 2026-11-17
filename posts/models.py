from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    """A campus post that can be a note, lost/found item, event, announcement, or help request."""

    # ── Category choices ──
    CATEGORY_CHOICES = [
        ('notes', 'Notes & Resources'),
        ('lost_found', 'Lost & Found'),
        ('events', 'Events'),
        ('announcements', 'Announcements'),
        ('student_help', 'Student Help'),
    ]

    # ── Status choices ──
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    # ── Lost/Found type choices ──
    LOST_FOUND_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    # ── Core fields ──
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    file = models.FileField(upload_to='posts/files/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # ── Lost & Found specific fields ──
    lost_found_type = models.CharField(
        max_length=5,
        choices=LOST_FOUND_CHOICES,
        blank=True,
        null=True,
        help_text='Whether the item was lost or found.',
    )
    item_location = models.CharField(
        max_length=200,
        blank=True,
        help_text='Where the item was lost or found.',
    )
    item_date = models.DateField(
        blank=True,
        null=True,
        help_text='When the item was lost or found.',
    )

    # ── Event specific fields ──
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)
    event_location = models.CharField(max_length=200, blank=True)

    # ── Timestamps ──
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})

    def get_category_display_short(self):
        """Return clean short label."""
        labels = {
            'notes': 'Notes',
            'lost_found': 'Lost & Found',
            'events': 'Events',
            'announcements': 'Announcements',
            'student_help': 'Help',
        }
        return labels.get(self.category, self.category)

    def get_category_icon(self):
        """Return Bootstrap icon class."""
        icons = {
            'notes': 'bi-journal-bookmark-fill',
            'lost_found': 'bi-binoculars-fill',
            'events': 'bi-ticket-perforated-fill',
            'announcements': 'bi-megaphone-fill',
            'student_help': 'bi-people-fill',
        }
        return icons.get(self.category, 'bi-file-earmark-text-fill')

    def get_category_emoji(self):
        """Fallback for any legacy reference."""
        return self.get_category_icon()

    @property
    def short_description(self):
        """Return a truncated description for card previews."""
        if len(self.description) > 120:
            return self.description[:120] + '…'
        return self.description


class Report(models.Model):
    """A report filed against a post by a student."""

    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Information'),
        ('other', 'Other'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_filed',
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True, help_text='Optional additional details.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Prevent the same user from reporting the same post twice
        unique_together = ['post', 'reporter']
        verbose_name = 'report'
        verbose_name_plural = 'reports'

    def __str__(self):
        return f'Report on "{self.post.title}" by {self.reporter}'

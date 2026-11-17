from django.contrib import admin
from .models import Post, Report


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for posts."""

    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description', 'author__full_name', 'author__email']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('author', 'category', 'title', 'description', 'status')}),
        ('Media', {'fields': ('image', 'file')}),
        ('Lost & Found Details', {
            'fields': ('lost_found_type', 'item_location', 'item_date'),
            'classes': ('collapse',),
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_time', 'event_location'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin configuration for reports."""

    list_display = ['get_post_title', 'reporter', 'reason', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['post__title', 'reporter__full_name', 'reporter__email', 'details']
    readonly_fields = ['created_at']
    list_per_page = 25

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post'
    get_post_title.admin_order_field = 'post__title'

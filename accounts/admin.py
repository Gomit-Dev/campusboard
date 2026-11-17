from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    """Admin configuration for the Student model."""

    model = Student
    list_display = ['email', 'full_name', 'role', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'full_name']
    ordering = ['-date_joined']

    # Fieldsets for the change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role')}),
        ('Campus Status', {'fields': ('is_verified',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_verified'),
        }),
    )

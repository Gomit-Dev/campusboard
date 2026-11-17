"""
Root URL configuration for CampusBoard.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import (
    home_view,
    admin_dashboard_view,
    admin_delete_post_view,
    admin_dismiss_report_view,
    admin_delete_user_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', include('posts.urls', namespace='posts')),

    # ── Admin Panel (custom, separate from Django admin) ──
    path('panel/', admin_dashboard_view, name='admin_dashboard'),
    path('panel/post/<int:pk>/delete/', admin_delete_post_view, name='admin_delete_post'),
    path('panel/report/<int:pk>/dismiss/', admin_dismiss_report_view, name='admin_dismiss_report'),
    path('panel/user/<int:pk>/delete/', admin_delete_user_view, name='admin_delete_user'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

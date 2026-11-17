from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('browse/', views.browse_view, name='browse'),
    path('create/', views.post_create_view, name='create'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    path('<int:pk>/', views.post_detail_view, name='detail'),
    path('<int:pk>/edit/', views.post_edit_view, name='edit'),
    path('<int:pk>/delete/', views.post_delete_view, name='delete'),
    path('<int:pk>/report/', views.report_post_view, name='report'),
]

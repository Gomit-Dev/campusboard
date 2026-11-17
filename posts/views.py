from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden

from .models import Post, Report
from .forms import PostForm, ReportForm

Student = get_user_model()
POSTS_PER_PAGE = 12

# ── Category metadata for templates ──
CATEGORY_META = {
    'notes': {
        'icon': 'bi-journal-bookmark-fill',
        'name': 'Notes & Resources',
        'description': 'Share study materials, PDFs, and exam papers',
    },
    'lost_found': {
        'icon': 'bi-binoculars-fill',
        'name': 'Lost & Found',
        'description': 'Report lost items or help return found ones',
    },
    'events': {
        'icon': 'bi-ticket-perforated-fill',
        'name': 'Campus Events',
        'description': 'Workshops, fests, hackathons, and more',
    },
    'announcements': {
        'icon': 'bi-megaphone-fill',
        'name': 'Announcements',
        'description': 'Campus notices and important updates',
    },
    'student_help': {
        'icon': 'bi-people-fill',
        'name': 'Student Help',
        'description': 'Ask questions, find teammates, get help',
    },
}


# ═══════════════════════════════════════════════
#  ADMIN DASHBOARD (staff only)
# ═══════════════════════════════════════════════

@staff_member_required
def admin_dashboard_view(request):
    """Admin panel with platform-wide stats, recent reports, and moderation tools."""

    # ── Platform stats ──
    total_students = Student.objects.filter(role=Student.ROLE_STUDENT).count()
    total_teachers = Student.objects.filter(role=Student.ROLE_TEACHER).count()
    total_posts = Post.objects.count()
    active_posts = Post.objects.filter(status='active').count()
    total_reports = Report.objects.count()
    pending_reports = Report.objects.select_related('post', 'reporter').order_by('-created_at')

    # ── Posts by category ──
    category_stats = (
        Post.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    category_labels = dict(Post.CATEGORY_CHOICES)
    for stat in category_stats:
        stat['label'] = category_labels.get(stat['category'], stat['category'])

    # ── Posts by status ──
    status_stats = (
        Post.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    status_labels = dict(Post.STATUS_CHOICES)
    for stat in status_stats:
        stat['label'] = status_labels.get(stat['status'], stat['status'])

    # ── Recent posts (for moderation) ──
    recent_posts = Post.objects.select_related('author').order_by('-created_at')[:10]

    # ── Reported posts (posts with at least one report) ──
    reported_posts = (
        Post.objects
        .annotate(report_count=Count('reports'))
        .filter(report_count__gt=0)
        .select_related('author')
        .order_by('-report_count')[:10]
    )

    # ── Recent students/teachers & User Management ──
    user_query = request.GET.get('user_q', '').strip()
    user_role_filter = request.GET.get('user_role', '').strip()

    members_qs = Student.objects.annotate(post_count=Count('posts')).order_by('-date_joined')
    if user_query:
        members_qs = members_qs.filter(
            Q(email__icontains=user_query) | Q(full_name__icontains=user_query)
        )
    if user_role_filter in [Student.ROLE_STUDENT, Student.ROLE_TEACHER, Student.ROLE_ADMIN]:
        members_qs = members_qs.filter(role=user_role_filter)

    recent_students = members_qs[:50]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_posts': total_posts,
        'active_posts': active_posts,
        'total_reports': total_reports,
        'category_stats': category_stats,
        'status_stats': status_stats,
        'recent_posts': recent_posts,
        'reported_posts': reported_posts,
        'pending_reports': pending_reports[:15],
        'recent_students': recent_students,
        'user_query': user_query,
        'user_role_filter': user_role_filter,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def admin_delete_user_view(request, pk):
    """Allow admin/staff to delete a student or teacher (user management)."""
    target_user = get_object_or_404(Student, pk=pk)

    # Disallow deleting own account
    if target_user == request.user:
        messages.error(request, 'You cannot delete your own admin account.')
        return redirect('admin_dashboard')

    # Guard: only superusers can delete other superusers
    if target_user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Only superusers can delete another superuser account.')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        user_name = target_user.full_name or target_user.email
        user_role = target_user.get_role_display()
        target_user.delete()
        messages.success(request, f'{user_role} account "{user_name}" has been deleted.')
        return redirect('admin_dashboard')

    post_count = target_user.posts.count()
    context = {
        'target_user': target_user,
        'post_count': post_count,
    }
    return render(request, 'admin_panel/confirm_delete_user.html', context)


@staff_member_required
def admin_delete_post_view(request, pk):
    """Allow admin/staff to delete any post (moderation)."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" has been removed.')
        return redirect('admin_dashboard')

    return render(request, 'admin_panel/confirm_delete.html', {'post': post})


@staff_member_required
def admin_dismiss_report_view(request, pk):
    """Dismiss (delete) a report."""
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report dismissed.')
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')


def home_view(request):
    """Dashboard homepage with search, categories, and recent posts."""
    query = request.GET.get('q', '').strip()

    if query:
        recent_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            status='active',
        ).select_related('author')[:12]
    else:
        recent_posts = Post.objects.filter(
            status='active'
        ).select_related('author')[:8]

    # Category data with icons and descriptions
    categories = []
    for value, label in Post.CATEGORY_CHOICES:
        count = Post.objects.filter(category=value, status='active').count()
        meta = CATEGORY_META.get(value, {})
        categories.append({
            'value': value,
            'label': label,
            'icon': meta.get('icon', 'bi-file-earmark-text-fill'),
            'name': meta.get('name', label),
            'description': meta.get('description', ''),
            'count': count,
        })

    context = {
        'recent_posts': recent_posts,
        'categories': categories,
        'search_query': query,
    }
    return render(request, 'home.html', context)


def browse_view(request):
    """Browse all posts with search, filter, sort, and pagination."""
    posts = Post.objects.select_related('author')

    # ── Search ──
    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # ── Filter by category ──
    category = request.GET.get('category', '').strip()
    valid_categories = dict(Post.CATEGORY_CHOICES)
    if category and category in valid_categories:
        posts = posts.filter(category=category)

    # ── Filter by status ──
    status = request.GET.get('status', '').strip()
    valid_statuses = dict(Post.STATUS_CHOICES)
    if status and status in valid_statuses:
        posts = posts.filter(status=status)

    # ── Filter by Lost/Found type ──
    lf_type = request.GET.get('lf_type', '').strip()
    valid_lf = dict(Post.LOST_FOUND_CHOICES)
    if lf_type and lf_type in valid_lf:
        posts = posts.filter(lost_found_type=lf_type)

    # ── Sort ──
    sort = request.GET.get('sort', 'newest').strip()
    if sort == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    # ── Total before pagination ──
    total_count = posts.count()

    # ── Pagination ──
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'total_count': total_count,
        'search_query': query,
        'selected_category': category,
        'selected_status': status,
        'selected_lf_type': lf_type,
        'selected_sort': sort,
        'category_choices': Post.CATEGORY_CHOICES,
        'status_choices': Post.STATUS_CHOICES,
        'lf_choices': Post.LOST_FOUND_CHOICES,
        'selected_category_label': valid_categories.get(category, ''),
        'selected_status_label': valid_statuses.get(status, ''),
    }
    return render(request, 'posts/browse.html', context)


def post_detail_view(request, pk):
    """Display a single post with all details."""
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)

    # Check if the current user has already reported this post
    already_reported = False
    is_own_post = False
    if request.user.is_authenticated:
        already_reported = Report.objects.filter(
            post=post, reporter=request.user
        ).exists()
        is_own_post = (post.author == request.user)

    context = {
        'post': post,
        'already_reported': already_reported,
        'is_own_post': is_own_post,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def post_create_view(request):
    """Create a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(user=request.user)

    return render(request, 'posts/create.html', {'form': form})


@login_required
def post_edit_view(request, pk):
    """Edit an existing post. Only the author can edit."""
    post = get_object_or_404(Post, pk=pk)

    # Authorization check
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden('You do not have permission to edit this post.')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(instance=post, user=request.user)

    return render(request, 'posts/edit.html', {'form': form, 'post': post})


@login_required
def post_delete_view(request, pk):
    """Delete a post with confirmation. Only the author can delete."""
    post = get_object_or_404(Post, pk=pk)

    # Authorization check
    if post.author != request.user:
        return HttpResponseForbidden('You do not have permission to delete this post.')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('posts:my_posts')

    return render(request, 'posts/delete.html', {'post': post})


@login_required
def my_posts_view(request):
    """Show the current user's posts with statistics and pagination."""
    user_posts = Post.objects.filter(author=request.user)

    total_posts = user_posts.count()
    active_posts = user_posts.filter(status='active').count()
    resolved_posts = user_posts.filter(status='resolved').count()

    posts_list = user_posts.order_by('-created_at')
    paginator = Paginator(posts_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/my_posts.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'total_posts': total_posts,
        'active_posts': active_posts,
        'resolved_posts': resolved_posts,
    })


@login_required
def report_post_view(request, pk):
    """Report a post."""
    post = get_object_or_404(Post, pk=pk)

    # Prevent reporting own post
    if post.author == request.user:
        messages.warning(request, 'You cannot report your own post.')
        return redirect('posts:detail', pk=post.pk)

    # Check if already reported
    if Report.objects.filter(post=post, reporter=request.user).exists():
        messages.warning(request, 'You have already reported this post.')
        return redirect('posts:detail', pk=post.pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.reporter = request.user
            report.save()
            messages.success(request, 'Thank you. Your report has been submitted.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = ReportForm()

    return render(request, 'posts/report.html', {'form': form, 'post': post})

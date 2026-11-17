from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import StudentRegistrationForm, StudentLoginForm, ProfileUpdateForm


def register_view(request):
    """Handle student registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            login(request, student)
            messages.success(request, f'Welcome to CampusBoard, {student.get_short_name()}! ✓ Campus Student')
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle student login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_short_name()}!')
            # Redirect to 'next' parameter if provided, otherwise home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = StudentLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle student logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Display and update student profile."""
    student = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=student)

    # Get post statistics
    total_posts = student.posts.count()
    active_posts = student.posts.filter(status='active').count()

    context = {
        'form': form,
        'total_posts': total_posts,
        'active_posts': active_posts,
    }
    return render(request, 'accounts/profile.html', context)

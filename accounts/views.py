from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, CustomUser
from jobs.models import Job, JobApplicant
from .forms import ProfileForm


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed in.')
        return redirect('posts:post-list')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not all([email, username, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})

        # Username validation
        if len(username) < 3 or not username.isalnum():
            messages.error(request, 'Username must be at least 3 characters long and contain only letters and numbers.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})

        # Password validation
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})

        # Check existing users
        try:
            if CustomUser.objects.filter(email__iexact=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'auth/signup.html', {'username': username})
            if CustomUser.objects.filter(username__iexact=username).exists():
                messages.error(request, 'This username is already taken.')
                return render(request, 'auth/signup.html', {'email': email})

            # Create user
            user = CustomUser.objects.create_user(email=email.lower(), username=username, password=password)
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('auth:signin')

        except IntegrityError:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'auth/signup.html', {'email': email, 'username': username})

    return render(request, 'auth/signup.html')


def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            # Redirect based on profile existence
            if hasattr(user, 'profile'):
                return redirect('posts:post-list')
            else:
                return redirect('accounts:profile_create')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/signin.html')


@login_required
def profile_create_view(request):
    user = request.user
    if hasattr(user, 'profile'):
        return redirect('accounts:profile_view')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('posts:post-list')
    else:
        form = ProfileForm()

    return render(request, 'auth/profile_create.html', {'form': form})


@login_required
def profile_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        messages.info(request, 'Please complete your profile first.')
        return redirect('accounts:profile_create')

    user = request.user
    context = {'user': user, 'profile': profile}

    if user.is_staff:
        context['jobs_created'] = Job.objects.filter(user=user)
    else:
        jobs_applied = JobApplicant.objects.filter(user=user).select_related('job')
        context['jobs_applied'] = [ja.job for ja in jobs_applied]

    return render(request, 'auth/profile_view.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('auth:signin')

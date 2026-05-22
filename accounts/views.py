  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import User, DeveloperLog
from .forms import ProfileUpdateForm, DeveloperLogForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
        'can_access_twelfth': request.user.can_access_level('twelfth'),
        'can_access_graduation': request.user.can_access_level('graduation'),
        'can_access_interview': request.user.can_access_level('interview'),
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def verify_email_view(request):
    if request.user.email_verified:
        return redirect('dashboard:dashboard')
    return render(request, 'accounts/verify_email.html')

@login_required
def verify_email_token(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        if user == request.user:
            user.email_verified = True
            user.save()
            messages.success(request, 'Email verified successfully.')
            return redirect('dashboard:dashboard')
    except User.DoesNotExist:
        pass
    messages.error(request, 'Invalid verification link.')
    return redirect('accounts:verify_email')

@login_required
def resend_verification(request):
    if not request.user.email_verified:
        verification_url = request.build_absolute_uri(
            reverse('accounts:verify_email_token', args=[request.user.email_verification_token])
        )
        send_mail(
            'Verify your EntreSkill Hub account',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, 'Verification email sent. Check your inbox.')
    return redirect('accounts:verify_email')

@login_required
def developer_logs_view(request):
    if request.user.role != 'developer':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:dashboard')
    
    logs = DeveloperLog.objects.filter(user=request.user)
    return render(request, 'accounts/developer_logs.html', {'logs': logs})

@login_required
def add_developer_log(request):
    if request.user.role != 'developer':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = DeveloperLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Log added successfully.')
            return redirect('accounts:developer_logs')
    else:
        form = DeveloperLogForm()
    
    return render(request, 'accounts/add_developer_log.html', {'form': form})
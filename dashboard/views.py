from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
import os

@login_required
def dashboard_view(request):
    user = request.user
    
    progress_data = {
        'tenth': {
            'percentage': user.tenth_percentage,
            'completed': user.tenth_completed,
            'unlocked': True,
            'certificate': user.tenth_certificate,
        },
        'twelfth': {
            'percentage': user.twelfth_percentage,
            'completed': user.twelfth_completed,
            'unlocked': user.can_access_level('twelfth'),
            'certificate': user.twelfth_certificate,
        },
        'graduation': {
            'percentage': user.graduation_percentage,
            'completed': user.graduation_completed,
            'unlocked': user.can_access_level('graduation'),
            'certificate': user.graduation_certificate,
        },
        'interview': {
            'unlocked': user.can_access_level('interview'),
        }
    }
    
    overall_progress = round(
        (user.tenth_percentage + user.twelfth_percentage + user.graduation_percentage) / 3, 1
    )
    
    context = {
        'progress_data': progress_data,
        'overall_progress': overall_progress,
        'user': user,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def download_certificate(request, level):
    user = request.user
    
    certificate_field = None
    if level == '10th' and user.tenth_completed:
        certificate_field = user.tenth_certificate
    elif level == '12th' and user.twelfth_completed:
        certificate_field = user.twelfth_certificate
    elif level == 'graduation' and user.graduation_completed:
        certificate_field = user.graduation_certificate
    else:
        messages.error(request, 'Certificate not available yet. Score 70 percent to unlock.')
        return redirect('dashboard:dashboard')
    
    if not certificate_field or not os.path.exists(certificate_field.path):
        raise Http404('Certificate not found')
    
    with open(certificate_field.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={level}_certificate.pdf'
        return response
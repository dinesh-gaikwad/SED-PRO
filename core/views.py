  
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from education.models import Course
from business.models import BusinessIdea

def home_view(request):
    featured_courses = Course.objects.filter(is_featured=True)[:3]
    featured_ideas = BusinessIdea.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'featured_courses': featured_courses,
        'featured_ideas': featured_ideas,
        'total_students': 5000,
        'total_courses': Course.objects.count(),
        'certificates_issued': 1200,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Add email sending logic here
        messages.success(request, 'Message sent successfully. We will contact you soon.')
        return redirect('core:contact')
    return render(request, 'core/contact.html')
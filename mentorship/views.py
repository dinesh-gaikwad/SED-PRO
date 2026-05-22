from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Mentor, MentorshipSession

@login_required
def mentor_list(request):
    mentors = Mentor.objects.filter(is_active=True)
    context = {'mentors': mentors}
    return render(request, 'mentorship/mentor_list.html', context)

@login_required
def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True)
    available_slots = generate_time_slots()
    context = {
        'mentor': mentor,
        'available_slots': available_slots,
    }
    return render(request, 'mentorship/mentor_detail.html', context)

@login_required
def book_session(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        topic = request.POST.get('topic')
        
        scheduled_at = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        session = MentorshipSession.objects.create(
            student=request.user,
            mentor=mentor,
            scheduled_at=scheduled_at,
            topic=topic,
            status='scheduled'
        )
        messages.success(request, f'Session booked with {mentor.name} for {scheduled_at.strftime("%B %d, %I:%M %p")}')
        return redirect('mentorship:my_sessions')
    
    return redirect('mentorship:mentor_detail', mentor_id=mentor_id)

@login_required
def mentorship_session(request, session_id):
    session = get_object_or_404(MentorshipSession, id=session_id, student=request.user)
    context = {'session': session}
    return render(request, 'mentorship/session.html', context)

@login_required
def my_sessions(request):
    upcoming = MentorshipSession.objects.filter(
        student=request.user,
        scheduled_at__gte=timezone.now()
    ).order_by('scheduled_at')
    
    past = MentorshipSession.objects.filter(
        student=request.user,
        scheduled_at__lt=timezone.now()
    ).order_by('-scheduled_at')[:5]
    
    context = {
        'upcoming': upcoming,
        'past': past,
    }
    return render(request, 'mentorship/my_sessions.html', context)

def generate_time_slots():
    slots = []
    base_date = timezone.now().date() + timedelta(days=1)
    for day in range(7):
        current_date = base_date + timedelta(days=day)
        for hour in [10, 11, 14, 15, 16, 17]:
            slots.append({
                'date': current_date,
                'time': f"{hour:02d}:00",
            })
    return slots
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InterviewSession, InterviewQuestion, InterviewAnswer
import json
import random

@login_required
def interview_home(request):
    if not request.user.can_access_level('interview'):
        return render(request, 'interview/locked.html')
    
    sessions = InterviewSession.objects.filter(user=request.user).order_by('-created_at')
    context = {'sessions': sessions}
    return render(request, 'interview/home.html', context)

@login_required
def start_interview(request):
    if not request.user.can_access_level('interview'):
        return redirect('interview:interview')
    
    session = InterviewSession.objects.create(
        user=request.user,
        interview_type=request.GET.get('type', 'hr'),
        status='active'
    )
    
    questions = InterviewQuestion.objects.filter(interview_type=session.interview_type).order_by('?')[:5]
    for q in questions:
        InterviewAnswer.objects.create(session=session, question=q)
    
    return redirect('interview:interview_session', session_id=session.id)

@login_required
def interview_session(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    answers = session.answers.select_related('question').all()
    
    current_answer = answers.filter(user_answer='').first()
    
    context = {
        'session': session,
        'answers': answers,
        'current_answer': current_answer,
        'progress': int((answers.filter(user_answer__gt='').count() / answers.count()) * 100)
    }
    return render(request, 'interview/session.html', context)

@login_required
@csrf_exempt
def submit_answer(request, session_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        answer_id = data.get('answer_id')
        user_answer = data.get('answer')
        
        answer = get_object_or_404(InterviewAnswer, id=answer_id, session__user=request.user)
        answer.user_answer = user_answer
        answer.feedback = generate_ai_feedback(user_answer, answer.question.correct_answer)
        answer.score = calculate_score(user_answer, answer.question.correct_answer)
        answer.save()
        
        return JsonResponse({'status': 'success', 'feedback': answer.feedback, 'score': answer.score})
    return JsonResponse({'status': 'error'})

@login_required
def interview_result(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    session.status = 'completed'
    session.overall_score = round(sum(a.score for a in session.answers.all()) / session.answers.count(), 1)
    session.save()
    
    context = {'session': session}
    return render(request, 'interview/result.html', context)

def generate_ai_feedback(user_answer, correct_answer):
    if len(user_answer.strip()) < 10:
        return 'Your answer is too short. Try to elaborate with examples.'
    if correct_answer.lower() in user_answer.lower():
        return 'Good answer. You covered the key point.'
    return 'Decent attempt. Consider mentioning key terms related to the question.'

def calculate_score(user_answer, correct_answer):
    user_words = set(user_answer.lower().split())
    correct_words = set(correct_answer.lower().split())
    overlap = len(user_words.intersection(correct_words))
    score = min(100, int((overlap / max(len(correct_words), 1)) * 100))
    return max(score, 30)
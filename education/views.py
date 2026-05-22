  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Exam, Question, UserExamResult
from .tasks import generate_certificate_task

@login_required
def education_home(request):
    courses = Course.objects.filter(is_active=True)
    context = {
        'courses': courses,
        'user': request.user,
        'can_access_twelfth': request.user.can_access_level('twelfth'),
        'can_access_graduation': request.user.can_access_level('graduation'),
        'can_access_interview': request.user.can_access_level('interview'),
    }
    return render(request, 'education/home.html', context)

@login_required
def course_detail(request, level):
    course = get_object_or_404(Course, level=level, is_active=True)
    
    if level == '12th' and not request.user.can_access_level('twelfth'):
        messages.error(request, 'Score 70 percent in 10th to unlock this course.')
        return redirect('education:education_home')
    if level == 'graduation' and not request.user.can_access_level('graduation'):
        messages.error(request, 'Score 70 percent in 12th to unlock this course.')
        return redirect('education:education_home')
    
    modules = course.modules.all()
    exam = getattr(course, 'exam', None)
    
    context = {
        'course': course,
        'modules': modules,
        'exam': exam,
    }
    return render(request, 'education/course_detail.html', context)

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        return redirect('education:submit_exam', exam_id=exam_id)
    
    context = {
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'education/take_exam.html', context)

@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    correct = 0
    for q in questions:
        user_answer = request.POST.get(f'question_{q.id}')
        if user_answer == q.correct_option:
            correct += 1
    
    score = round((correct / len(questions)) * 100, 2)
    passed = score >= exam.passing_percentage
    
    result, created = UserExamResult.objects.update_or_create(
        user=request.user,
        exam=exam,
        defaults={'score': score, 'passed': passed}
    )
    
    request.user.update_level_percentage(exam.course.level, score)
    
    if passed:
        generate_certificate_task.delay(request.user.id, exam.course.level)
        messages.success(request, f'Congratulations! You scored {score} percent. Certificate will be emailed to you.')
    else:
        messages.warning(request, f'You scored {score} percent. You need 70 percent to pass and unlock next level.')
    
    return redirect('dashboard:dashboard')
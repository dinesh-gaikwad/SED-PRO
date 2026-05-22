from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InterviewSession(models.Model):
    TYPE_CHOICES = [
        ('hr', 'HR Round'),
        ('technical', 'Technical Round'),
        ('behavioral', 'Behavioral'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    interview_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='hr')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    overall_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

class InterviewQuestion(models.Model):
    interview_type = models.CharField(max_length=20, choices=InterviewSession.TYPE_CHOICES)
    question_text = models.TextField()
    correct_answer = models.TextField()
    
    def __str__(self):
        return self.question_text[:100]

class InterviewAnswer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    score = models.IntegerField(default=0)
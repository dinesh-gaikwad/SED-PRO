from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Mentor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    expertise = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='mentors/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

class MentorshipSession(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_sessions')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='sessions')
    scheduled_at = models.DateTimeField()
    topic = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
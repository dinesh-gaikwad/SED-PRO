from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('developer', 'Developer'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # Progress tracking for 70% gate system
    tenth_percentage = models.FloatField(default=0.0)
    tenth_completed = models.BooleanField(default=False)
    tenth_certificate = models.FileField(upload_to='certificates/10th/', null=True, blank=True)
    
    twelfth_percentage = models.FloatField(default=0.0)
    twelfth_completed = models.BooleanField(default=False)
    twelfth_certificate = models.FileField(upload_to='certificates/12th/', null=True, blank=True)
    
    graduation_percentage = models.FloatField(default=0.0)
    graduation_completed = models.BooleanField(default=False)
    graduation_certificate = models.FileField(upload_to='certificates/graduation/', null=True, blank=True)
    
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def can_access_level(self, level):
        if level == 'tenth':
            return True
        if level == 'twelfth':
            return self.tenth_completed and self.tenth_percentage >= 70.0
        if level == 'graduation':
            return self.twelfth_completed and self.twelfth_percentage >= 70.0
        if level == 'interview':
            return self.graduation_completed and self.graduation_percentage >= 70.0
        return False
    
    def update_level_percentage(self, level, percentage):
        if level == '10th':
            self.tenth_percentage = percentage
            if percentage >= 70.0 and not self.tenth_completed:
                self.tenth_completed = True
        elif level == '12th':
            self.twelfth_percentage = percentage
            if percentage >= 70.0 and not self.twelfth_completed:
                self.twelfth_completed = True
        elif level == 'graduation':
            self.graduation_percentage = percentage
            if percentage >= 70.0 and not self.graduation_completed:
                self.graduation_completed = True
        self.save()
    
    def __str__(self):
        return self.email

class DeveloperLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dev_logs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    code_snippet = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
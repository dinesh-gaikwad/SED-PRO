from django import forms
from .models import User, DeveloperLog

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class DeveloperLogForm(forms.ModelForm):
    class Meta:
        model = DeveloperLog
        fields = ['title', 'description', 'code_snippet']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'code_snippet': forms.Textarea(attrs={'rows': 6}),
        }
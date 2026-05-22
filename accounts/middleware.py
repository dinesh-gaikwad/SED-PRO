from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('account_login'),
            reverse('account_signup'),
            reverse('account_logout'),
            reverse('accounts:verify_email'),
            reverse('accounts:resend_verification'),
            '/admin/',
        ]
    
    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path
            if not any(path.startswith(url) for url in self.exempt_urls):
                if not request.user.email_verified:
                    messages.warning(request, 'Please verify your email to access all features.')
                    return redirect('accounts:verify_email')
        
        response = self.get_response(request)
        return response
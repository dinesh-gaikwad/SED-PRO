  
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('verify/<uuid:token>/', views.verify_email_token, name='verify_email_token'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('developer-logs/', views.developer_logs_view, name='developer_logs'),
    path('developer-logs/add/', views.add_developer_log, name='add_developer_log'),
]
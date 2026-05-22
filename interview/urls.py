  
from django.urls import path
from . import views

app_name = 'interview'

urlpatterns = [
    path('', views.interview_home, name='interview'),
    path('start/', views.start_interview, name='start_interview'),
    path('session/<int:session_id>/', views.interview_session, name='interview_session'),
    path('session/<int:session_id>/submit/', views.submit_answer, name='submit_answer'),
    path('session/<int:session_id>/result/', views.interview_result, name='interview_result'),
]
  
from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('home/', views.education_home, name='education_home'),
    path('course/<str:level>/', views.course_detail, name='course_detail'),
    path('exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('exam/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
]
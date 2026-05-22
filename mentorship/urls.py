  
from django.urls import path
from . import views

app_name = 'mentorship'

urlpatterns = [
    path('', views.mentor_list, name='mentor_list'),
    path('mentor/<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
    path('book/<int:mentor_id>/', views.book_session, name='book_session'),
    path('session/<int:session_id>/', views.mentorship_session, name='mentorship_session'),
    path('my-sessions/', views.my_sessions, name='my_sessions'),
]
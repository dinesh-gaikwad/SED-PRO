from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    path('ideas/', views.ideas_view, name='ideas'),
    path('api/generate-ideas/', views.generate_ideas_api, name='generate_ideas_api'),
]
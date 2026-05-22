  
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('certificate/<str:level>/download/', views.download_certificate, name='download_certificate'),
]
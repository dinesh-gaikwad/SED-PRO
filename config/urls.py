  
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('education/', include('education.urls', namespace='education')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('business/', include('business.urls', namespace='business')),
    path('mentorship/', include('mentorship.urls', namespace='mentorship')),
    path('interview/', include('interview.urls', namespace='interview')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
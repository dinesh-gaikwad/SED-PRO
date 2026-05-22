  
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('entreskill_hub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'dashboard.tasks.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    'cleanup-old-sessions': {
        'task': 'accounts.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),
    },
}

app.conf.timezone = 'Asia/Kolkata'
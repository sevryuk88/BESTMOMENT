from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_feed.settings.dev')

app = Celery('video_feed')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




"""
app.conf.beat_schedule = {
    'update-top-videos-every-10-days': {
        'task': 'videos.tasks.update_top_videos',
        'schedule': crontab(day_of_month='*/10'),  # Каждые 10 дней
    },
}
"""
app.conf.beat_schedule = {
    'update-top-videos-every-minute': {
        'task': 'videos.tasks.update_top_videos',
        'schedule': crontab(minute='*/1'),  # <--- временно
    },
}

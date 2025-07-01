import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery('lunch_voting')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
import core.tasks.winner


app.conf.beat_schedule = {
    'calculate-winner-every-day-12pm':{
        'task': 'core.tasks.winner.run_daily_winner_calculation',
        'schedule': crontab(hour=12, minute=0),
        'args': ()
    }
}
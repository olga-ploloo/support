import os

import django
from celery import Celery

# from ticket.tasks import SCHEDULE as TICKET_SCHEDULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'support.settings')
django.setup()

app = Celery('support')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = TICKET_SCHEDULE
app.autodiscover_tasks()

import os

import django
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'support.settings')
django.setup()

app = Celery('support')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoWebProject2.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

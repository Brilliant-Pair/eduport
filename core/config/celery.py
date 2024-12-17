import os

from celery import Celery

# TODO: change this in production stage.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("config")
app.config_from_object("config.settings.local", namespace="CELERY")
app.autodiscover_tasks()

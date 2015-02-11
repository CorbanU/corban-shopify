from __future__ import absolute_import

import os

from celery import Celery
from configurations import importer
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

importer.install()

app = Celery('shopify')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

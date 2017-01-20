from .base import *  # noqa

from celery.schedules import crontab


SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

CELERY_BEAT_SCHEDULE = {
    'email_journal_vouchers_import': {
        'task': 'shopify.product.tasks.email_journal_vouchers_import',
        # Generate import file at 21:00 every night. This matches
        # the Shopify transaction cutoff at midnight EST.
        'schedule': crontab(minute=0, hour=21),
    }
}

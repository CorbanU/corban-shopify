from configurations import values

from celery.schedules import crontab

from .base import Base


class Production(Base):
    SECRET_KEY = values.SecretValue()

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', Base.TEMPLATE_LOADERS),
    )

    CELERYBEAT_SCHEDULE = {
        'email_journal_vouchers_import': {
            'task': 'product.tasks.email_journal_vouchers_import',
            'schedule': crontab(minute=0, hour=0),
        }
    }

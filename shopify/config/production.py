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
            # Generate import file at 21:00 every night. This matches
            # the Shopify transaction cutoff at midnight EST.
            'schedule': crontab(minute=0, hour=21),
        }
    }

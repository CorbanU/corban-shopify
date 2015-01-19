from configurations import values

from .base import Base


class Local(Base):
    DEBUG = values.BooleanValue(True)

    STATIC_URL = '/static/'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Base.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)

from .base import *  # noqa


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ('debug_toolbar',)

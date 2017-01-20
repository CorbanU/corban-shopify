import environ


root_dir = environ.Path(__file__) - 3
project_dir = root_dir.path('shopify')

env = environ.Env()
env.read_env('.env')

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
)

LOCAL_APPS = (
    'shopify.notification.apps.NotificationConfig',
    'shopify.product.apps.ProductConfig',
    'shopify.user.apps.UserConfig',
    'shopify.webhook.apps.WebhookConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

MIGRATION_MODULES = {}

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = env('DJANGO_SECRET_KEY')

FIXTURE_DIRS = (
    project_dir('fixtures'),
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = ''

DEFAULT_FROM_EMAIL = 'help@corban.edu'

ADMINS = (
    ('Jason Bittel', 'jbittel@corban.edu'),
    ('Brian Elliott', 'belliott@corban.edu'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://localhost/shopify'),
}

CACHES = {
    'default': env.cache('CACHE_URL', default='locmemcache://'),
}

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = False
USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            project_dir('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_ROOT = root_dir('assets')

STATIC_URL = env.str('DJANGO_STATIC_URL')

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = root_dir('media')
MEDIA_URL = '/media/'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(process)d] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'notification': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'product': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'webhook': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

BROKER_URL = 'redis://localhost:6379/1'

CELERY_RESULT_BACKEND = BROKER_URL
CELERY_DISABLE_RATE_LIMITS = True
CELERY_DEFAULT_QUEUE = 'shopify'

SHOPIFY_SHARED_SECRET = env('SHOPIFY_SHARED_SECRET')
SHOPIFY_API_KEY = env('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = env('SHOPIFY_PASSWORD')
SHOPIFY_SHARED_SECRET = env('SHOPIFY_SHARED_SECRET')
SHOPIFY_HOSTNAME = env('SHOPIFY_HOSTNAME')
SHOPIFY_CASH_ACCOUNT_NUMBER = env('SHOPIFY_CASH_ACCOUNT_NUMBER')

from pathlib import Path

import os
from dotenv import load_dotenv

import logging


logger = logging.getLogger(__name__)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'django_filters',

    'models_portal',
    'pages.apps.PagesConfig',
    'articles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'django_apscheduler'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                           'allauth.account.auth_backends.AuthenticationBackend']

WSGI_APPLICATION = 'news_portal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'format_debug': {
            'format': '{asctime}:<{levelname}> - {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
            'validate': True
        },
        'format_info': {
            'format': '{asctime}:(<{levelname}> <{module}>) - {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
            'validate': True
        },
        'format_warning': {
            'format': '{asctime}:(<{pathname}> <{levelname}>) - {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
            'validate': True
        },
        'format_error_critical': {
            'format': '{asctime}:(<{pathname}> <{levelname}>) - {message} [{exc_info}]',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
            'validate': True
        }
    },
    'handlers': {
        'debug_handler_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format_debug',
            'filters': ['debug_true', ]
        },
        'warning_handler_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'format_warning',
            'filters': ['debug_true', ]
        },
        'error_critical_console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'format_error_critical',
            'filters': ['debug_true', ]
        },
        'file_general_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'format_info',
            'filters': ['debug_false', ],
            'filename': 'logs/general.log'
        },
        'file_errors_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'format_error_critical',
            'filename': 'logs/error.log'
        },
        'file_security_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'format_info',
            'filename': 'logs/security.log'
        },
        'send_mail': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['debug_false', ],
            'formatter': 'format_warning'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['debug_handler_console',
                         'warning_handler_console',
                         'error_critical_console',
                         'file_general_log', ],
            'propagate': True
        },
        'django.request': {
            'handlers': ['file_errors_log',
                         'send_mail', ],
            'propagate': True
        },
        'django.server': {
            'handlers': ['file_errors_log',
                         'send_mail', ],
            'propagate': True
        },
        'django.template': {
            'handlers': ['file_errors_log', ],
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['file_errors_log', ],
            'propagate': True
        },
        'django.security': {
            'handlers': ['file_security_log', ],
            'propagate': True
        },
    }
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR/'static']

SITE_ID = 1

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/news/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'pages.forms.SignUpForm'}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

MANAGERS = []
ADMINS = [(os.getenv('ADMIN_NAME_1'), os.getenv('ADMIN_EMAIL_1')),
          (os.getenv('ADMIN_NAME_2'), os.getenv('ADMIN_EMAIL_2'))]
SERVER_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                      'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
                      'TIMEOUT': 15}}

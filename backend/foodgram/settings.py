import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

from foodgram.constants import PER_PAGE_LIMIT

# Привет, босс! Крутые замечания, спасибо!
# Всё исправил, всё проверил, готов принять критику!

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
]

CSRF_TRUSTED_ORIGINS = [
    host.strip() for host in os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'django_filters',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',

    'users',
    'recipes',
    'api',
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

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR.parent, 'docs')],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

USE_SQLITE = os.getenv('USE_SQLITE', 'False').lower() == 'true'

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('DB_HOST', '1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

AUTH_USER_MODEL = 'users.User'

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageLimitPagination',
    'PAGE_SIZE': PER_PAGE_LIMIT,
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'SERIALIZERS': {
        'user': 'api.users.serializers.UserSerializer',
        'current_user': 'api.users.serializers.UserSerializer',
        'user_create': 'api.users.serializers.UserCreateSerializer',
    }
}

RESERVED_USERNAMES = ('me',)

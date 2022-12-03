"""
Django settings for mysocial project.
Generated by 'django-admin startproject' using Django 3.1.6.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import json
import os
import sys
from pathlib import Path

import django_on_heroku
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8zox7ox(g#^5%*))!ywyjs1c9k3zwzpkefc1t$3r3ej19(20b*'

ALLOWED_HOSTS = ['127.0.0.1', 'socioecon.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'authors.apps.AuthorsConfig',
    'post.apps.PostConfig',
    'comment.apps.CommentConfig',
    'follow.apps.FollowsConfig',
    'tokens.apps.TokensConfig',
    'inbox.apps.InboxConfig',
    'likes.apps.LikesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'mylogger': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysocial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'staticfiles/')],
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

WSGI_APPLICATION = 'mysocial.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Our custom user
AUTH_USER_MODEL = "authors.Author"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
django_on_heroku.settings(locals())
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles/static')]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
CORS_ALLOW_CREDENTIALS = True

# later if the above causes issue
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # for localhost (REACT Default)
    'http://192.168.0.50:3000',  # for network
    'http://localhost:8000',  # for localhost (Development)
    'http://192.168.0.50:8000',  # for network (Development)
]

# from https://stackoverflow.com/a/72249293/17836168
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # for localhost (REACT Default)
    'http://192.168.0.50:3000',  # for network
    'http://localhost:8000',  # for localhost (Development)
    'http://192.168.0.50:8000',  # for network (Development)
]

CORS_ALLOW_HEADERS = default_headers + (
    'set-cookie',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'host',  # special header for team12
)

CORS_EXPOSE_HEADERS = [
    'set-cookie',
    'cookie',
]

# docs
SPECTACULAR_SETTINGS = {
    'TITLE': 'Sociocon API',
    'DESCRIPTION': 'Note: application/json is best supported by our servers so remember to toggle the Payload Content '
                   'type drop-down choice to application/json. Check out our [Github repository]('
                   'https://github.com/hgshah/cmput404-project) to file an Issue. Our main, stable endpoint is at '
                   'https://socioecon.herokuapp.com/',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}


"""
Heroku Config under!

Check out the settings page of Heroku, and look at the Config Vars section.
That's where we store the os.environ stuff!
"""

# keys

CURRENT_PORT = 8000
# if port was passed through command line
try:
    # from https://stackoverflow.com/a/48148250/17836168
    CURRENT_PORT = int(sys.argv[-1])
except:
    pass

CURRENT_DOMAIN_KEY = "CURRENT_DOMAIN"
CURRENT_DOMAIN = f"127.0.0.1:{CURRENT_PORT}"

if CURRENT_DOMAIN_KEY in os.environ:
    CURRENT_DOMAIN = os.environ[CURRENT_DOMAIN_KEY]

# remote config credentials
REMOTE_NODE_CREDENTIALS: dict = {}
REMOTE_NODE_CREDENTIALS_KEY = 'REMOTE_NODE_CREDENTIALS'
if REMOTE_NODE_CREDENTIALS_KEY in os.environ:
    REMOTE_NODE_CREDENTIALS = json.loads(os.environ[REMOTE_NODE_CREDENTIALS_KEY])


"""
Dictionary of domain/host and domain config (class NodeConfigBase) pair

Placed here to prevent circular dependencies
"""
REMOTE_CONFIG: dict = {}

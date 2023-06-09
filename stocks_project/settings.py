"""
Django settings for stocks_project project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
# Data from the environment file
if not os.environ.get("DEBUG"):
    print("Please specify DEBUG variable in .env file")
debug = False if os.environ.get('DEBUG').lower() == 'false' else True

if not os.environ.get("DATABASE_NAME"):
    print("Please specify DATABASE_NAME variable in .env file")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

if not os.environ.get("DATABASE_USERNAME"):
    print("Please specify DATABASE_PASSWORD variable in .env file")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")

if not os.environ.get("DATABASE_PASSWORD"):
    print("Please specify DATABASE_PASSWORD variable in .env file")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

if not os.environ.get("DATABASE_HOST"):
    print("Please specify 'DATABASE_HOST' variable in .env file")
DATABASE_HOST = os.environ.get("DATABASE_HOST")

if not os.environ.get("DATABASE_PORT"):
    print("Please specify 'DATABASE_PORT' variable in .env file")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

if not os.environ.get("JWT_ENCODING_ALGO"):
    print("Please specify JWT_ENCODING_ALGO' variable in .env file")
JWT_ENCODING_ALGO = os.environ.get("JWT_ENCODING_ALGO")

if not os.environ.get("JWT_ENCODING_SECRET_KEY"):
    print("Please specify 'JWT_ENCODING_SECRET_KEY' variable in .env file")
JWT_ENCODING_SECRET_KEY = os.environ.get("JWT_ENCODING_SECRET_KEY")

if not os.environ.get("JWT_TOKEN_EXPIRY_DELTA"):
    print("Please specify 'JWT_TOKEN_EXPIRY_DELTA' variable in .env file")
JWT_TOKEN_EXPIRY_DELTA = os.environ.get("JWT_TOKEN_EXPIRY_DELTA")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n-(9us7ygvesa%e9bp2k696hpd+b$*n$w7dl9u+oa9t73mf3*m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'stocks'
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

ROOT_URLCONF = 'stocks_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'stocks_project.wsgi.application'
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USERNAME,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "stocks.User"
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

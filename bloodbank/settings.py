"""
Django settings for bloodbank project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from django.core.mail.backends.smtp import EmailBackend
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-klea+6n_z3$ukkfq$g!ztvr51n2mcdz#y4&^(34+p_xh75%-h7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['blood-bank-management-aefj.onrender.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Ensure this is first
    'django.contrib.sessions.middleware.SessionMiddleware',  # Must come before AuthenticationMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # This should be after SessionMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',  # This should come after AuthenticationMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Optional, only if you're using caching
    'django.middleware.cache.FetchFromCacheMiddleware',  # Optional, only if you're using caching
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.staticfiles.middleware.StaticFilesMiddleware',  # Static files middleware (important for serving files)
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Optional: if using WhiteNoise for static file handling
]


ROOT_URLCONF = 'bloodbank.urls'

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

WSGI_APPLICATION = 'bloodbank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# settings.py

STATIC_URL = '/static/'

# For production, use STATIC_ROOT to collect all static files in one place
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use STATICFILES_DIRS for any additional static files during development (optional)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bloodbank/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this middleware for static file handling
    # Other middlewares
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # or the port your email service uses
EMAIL_USE_TLS = True  # or False if your email service uses SSL
EMAIL_HOST_USER = 'abloodbank8@gmail.com'  # your email address
EMAIL_HOST_PASSWORD = 'escxzyqzeuhqzspo'  # your email password

# Replace the above placeholders with your actual email settings.

# Optionally, you can define additional settings such as email timeout, etc.
# EMAIL_TIMEOUT = None  # Set to a number of seconds if you want to specify a timeout for sending emails.

# Ensure you update the DEBUG setting accordingly for production.


# Ensure you update the ALLOWED_HOSTS setting with your production domain.


# Also, make sure to configure other necessary settings like DATABASES, etc., as needed for your project.

# Leave other settings as they are or modify them according to your project requirements.
"""
Django settings for nxt project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ac5c9b0r^)vtp4yd95nh0^kwgmtdw@@pcf@$z1ndlbv%p5i=wz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nxt.urls'

WSGI_APPLICATION = 'nxt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'corenxt',
        'USER': 'root',
        'PASSWORD':'23er45af45sg90n3n5082147mio7inoi',
        'HOST':'',
        'PORT':'',
        
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
APPEND_SLASH = False
ACCOUNT_ACTIVATION_DAYS = 2

# https://docs.djangoproject.com/en/dev/howto/static-files/

LOGIN_REDIRECT_URL = '/'
STATICFILES_DIRS = os.path.join(BASE_DIR,"static"),
STATIC_URL = '/static/'
TEMPLATE_DIRS=(os.path.join(BASE_DIR,'templates'),os.path.join(BASE_DIR,'registration'))

"""
Django settings for xiencias project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aov3i5q*e1(1dbwqp^3ehsdun2ygfz2wmxd0*x87zrih@mvq6='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []




# Application definition


PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, '../templates'),)

MEDIA_ROOT = os.path.join(PROJECT_PATH, '/var/www/html/')

MEDIA_URL = '/var/www/html/'

STATICFILES_DIRS = (
    
    os.path.join(BASE_DIR, "static"),)

MEDIA_URL = '/var/www/html/'


INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appxiencias',
    'monitoreo',
    'corsheaders',
    #'preventconcurrentlogins',
  
)

MIDDLEWARE_CLASSES = (

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    
    
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'xiencias.urls'

WSGI_APPLICATION = 'xiencias.wsgi.application'

#APPEND_SLASH = False

#andrade terrazas sandra
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'xiencias',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },
    'beyond': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'beyond',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },

    'tecnolink': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'tecnolink',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },

    'blaster_beyond': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'blaster_beyond',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3_b3y0nd',
        'HOST': '10.13.50.100',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },
     'MTC': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'MTC',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },

     'CMYVAL': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'CMYVAL',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },


     'konnect': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'konnect',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },

    'GNU': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'gnu',
        'USER': 'root',
        'PASSWORD': 'd4t4B4$3*',
        'HOST': 'xiencias.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },




}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
    ('es', _('Spanish')),
)


TEMPLATE_CONTEXT_PROCESSORS =  (

    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

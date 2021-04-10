"""
Django settings for life_recorder project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import environ
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 2

env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, 'DOCKER')
)


# INFO: read heroku settings
ON_HEROKU = env('ENVIRONMENT') == 'HEROKU'
if ON_HEROKU:
    import dj_database_url
else:
    env_file = str(BASE_DIR.path('.env'))
    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'bootstrap4',
    'bootstrap_datepicker_plus',
    # 'hamlpy', # なくても動く
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms.apps.CmsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # INFO: For serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'life_recorder.urls'


TEMPLATES_LOADERS = (
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # INFO: loadersをセットしたときは、APP_DIRSを設定してはいけない模様
        # django.core.exceptions.ImproperlyConfigured: app_dirs must not be set when loaders is defined.
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': TEMPLATES_LOADERS,
        },
    },
]
if ON_HEROKU:
    TEMPLATES[0]['OPTIONS']['loaders'] = \
        ('django.template.loaders.cached.Loader', TEMPLATES_LOADERS),
# import pdb; pdb.set_trace()

WSGI_APPLICATION = 'life_recorder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if ON_HEROKU:
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': db_from_env
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'life_recorder',
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '',
            'TEST': {
                'NAME': 'life_record_test',
            },
        }
    }


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
# LANGUAGE_CODE = 'ja'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


if ON_HEROKU:
    # INFO: This must be set at the bottom of settings.py
    # https://devcenter.heroku.com/ja/articles/django-app-configuration
    django_heroku.settings(locals())

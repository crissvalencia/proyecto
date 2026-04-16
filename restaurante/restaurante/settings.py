"""
Django settings for restaurante project.
"""
from pathlib import Path
import django.db.backends.mysql.base

# Monkey patch to allow MariaDB 10.4 (Django 5 requires 10.6+)
original_check = django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported

def patched_check(self):
    try:
        original_check(self)
    except django.db.utils.NotSupportedError:
        pass  # Ignore version check failure

django.db.backends.mysql.base.DatabaseWrapper.check_database_version_supported = patched_check

# Patch features to disable RETURNING (requires MariaDB 10.5+)
from django.db.backends.mysql.features import DatabaseFeatures
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)




BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-341&98z@ow(%zg7j4k1b#(qlqnhdr*_u(%c=s&iqv2)be*@a&+'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion.config.apps.GestionConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'gestion.config.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'restaurante.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'gestion' / 'views'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurante.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'restaurante_db', 
        'USER': 'root',           
        'PASSWORD': 'eltilininsano', 
        'HOST': '127.0.0.1',      
        'PORT': '3308',           
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Ensure session expires when the user closes their browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

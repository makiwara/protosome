# -*- coding: utf-8 -*-

# попробуем вытащить из python path настройки хостов
try:
    from host_settings import *
except:
    try:
        from settings.hosts import *
    except:
        from protosome.settings.hosts import *

# настройка приложений
# installed apps directory
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'utils', 
]

#  Всякие полезные ништяки
DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = False

# admin information for debug emailing, etc.
ADMINS = (('makiwara', 'mendokusee@gmail.com'),)
MANAGERS = ADMINS

MEDIA_ROOT = HOST['PATH']+'/static/'
MEDIA_URL = '/static/'
SECRET_KEY = HOST['SECRET']
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    HOST['PATH']+'/templates',
)

# email configuration
try:
    from emails_settings import *
except:
    pass
# database configuration
try:
    from db_settings import *
except:
    IS_MYSQL=False
    DATABASE_ENGINE = 'sqlite3' 
    DATABASE_NAME = '@database.db'
    DATABASE_USER = ''           
    DATABASE_PASSWORD = ''       
    DATABASE_HOST = ''           
    DATABASE_PORT = ''

#---------------------------------
# other unaffected base configuration parts
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
ADMIN_MEDIA_PREFIX = '/admin-media/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

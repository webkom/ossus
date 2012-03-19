import os

DEBUG = True
TEMPLATE_DEBUG = True

BASE_PATH = os.path.dirname(__file__)

ADMINS = (
    ('Fredrik', 'fredrik@fncit.no'),
    )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project.db'
    }
}

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'no-nb'

AUTH_PROFILE_MODULE = 'core.UserProfile'

#STATIC FILES
STATIC_ROOT = BASE_PATH + '/static_media/'
STATIC_URL = '/static/'
MEDIA_ROOT = STATIC_URL
ADMIN_MEDIA_PREFIX = MEDIA_ROOT + 'admin/'

STATICFILES_DIRS = (
    BASE_PATH + '/files/',
    )

# Don't share this with anybody.
SECRET_KEY = 'zwvt#)va2#v&avbec*plq1!u4+an3o!rtmi(h6hchgvdxh95@7e'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',


    )

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'core',
    'app.backup',

    'south',
    'piston',

    )


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    )


TEMPLATE_DIRS = (
    BASE_PATH + "/templates",
    )
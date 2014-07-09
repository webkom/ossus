import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('frecar', 'fredrik@fncit.no'),
)

MANAGERS = ADMINS

LOGIN_REDIRECT_URL = "/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT_DIRECTORY + '/focusbackup.db'
    }
}

AUTH_PROFILE_MODULE = 'core.UserProfile'

URL_TO_SITE = "http://localhost:8000/"

#Used to script upload of new client files
PATH_LOCAL_FOCUSBACKUPCLIENT = "/Users/frecar/code/focusbackupclient/out/artifacts/"


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT_DIRECTORY, 'uploads')
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_ROOT_DIRECTORY, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT_DIRECTORY, 'files/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '-4d(=bk(k&amp;uzw$1_()l!y-mu&amp;yai=#&amp;(x%d&amp;oy7k*u_e(i#5=4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'focusbackup.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT_DIRECTORY + '/templates/',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'focusbackup',
    'focusbackup.core',
    'focusbackup.app.accounts',
    'focusbackup.app.client',
    'focusbackup.app.backup',
    'focusbackup.app.machine',
    'focusbackup.app.customer',
    'focusbackup.app.storage',
    'focusbackup.api',

    'django_extensions',
    'south'

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level': 'DEBUG',
            'class':'django.utils.log.NullHandler',
            },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['null'], # Quiet by default!
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

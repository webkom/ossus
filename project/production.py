from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

f = open('/home/frecar/passwords/db-backup-fncit.txt', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fncit_backup',
        'USER': 'root',
        'PASSWORD': DB_PASSWORD,
    }
}

STATIC_URL = '/static/'

#EMAIL DEBUG
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'focustimeno@gmail.com'
EMAIL_HOST_PASSWORD = '4th56y44g'
EMAIL_PORT = 587

DEBUG_EMAIL = "fredrik@fncit.no"
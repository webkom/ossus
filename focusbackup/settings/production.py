DEBUG = False
TEMPLATE_DEBUG = DEBUG

f = open('/var/passwords/focus24', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'HOST': '10.0.6.30',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'focus24',
        'USER': 'focus24',
        'PASSWORD': DB_PASSWORD,
        }
}

STATIC_URL = '/static/'

URL_TO_SITE = "http://focus24.no/"

#EMAIL DEBUG
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'focustimeno@gmail.com'
EMAIL_HOST_PASSWORD = '4th56y44g'
EMAIL_PORT = 587

DEBUG_EMAIL = "fredrik@fncit.no"
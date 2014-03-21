DEBUG = False
TEMPLATE_DEBUG = DEBUG

f = open('/var/passwords/focus24', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'HOST': '10.0.6.31',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'focus24',
        'USER': 'focus24',
        'PASSWORD': DB_PASSWORD,
        }
}

STATIC_URL = '/static/'
URL_TO_SITE = "http://focus24.no/"
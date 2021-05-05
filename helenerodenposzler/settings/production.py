from .base import *

DEBUG = False
SECRET_KEY = 'x*iawo25-30xi1suo-12!z23-ie)+frm7ue736x$akp39dk0hm'
BASE_URL = 'http://helelerodenposzler.com'
ALLOWED_HOSTS = ['*']

# reCaptcha settings:
RECAPTCHA_PUBLIC_KEY = '6LdmO8AaAAAAADp169DNvs3k_oj1YQH__sZpN8X8'
RECAPTCHA_PRIVATE_KEY = '6LdmO8AaAAAAAEzHD7lmCeObdLitHaNxJRM1kput'
NOCAPTCHA = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'helenerodenposzler',
        'USER': 'helene_admin',
        'PASSWORD': 'miaumiau2021',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
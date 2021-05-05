from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x*iawo25-30xi1suo-12!z23-ie)+frm7ue736x$akp39dk0hm'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

BASE_URL = 'http://helelerodenposzler.com'

# reCaptcha settings:
RECAPTCHA_PUBLIC_KEY = '6LdmO8AaAAAAADp169DNvs3k_oj1YQH__sZpN8X8'
RECAPTCHA_PRIVATE_KEY = '6LdmO8AaAAAAAEzHD7lmCeObdLitHaNxJRM1kput'
NOCAPTCHA = True


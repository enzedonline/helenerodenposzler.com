from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

# reCaptcha settings:
RECAPTCHA_PUBLIC_KEY = '6LdmO8AaAAAAADp169DNvs3k_oj1YQH__sZpN8X8'
RECAPTCHA_PRIVATE_KEY = '6LdmO8AaAAAAAEzHD7lmCeObdLitHaNxJRM1kput'
NOCAPTCHA = True

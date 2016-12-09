from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = '*z6o_48l9jfhgy6ppuc@yx#ys2s%$aszm%fip-jz*kl-bvnuf5'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS=['*']

try:
    from .local import *
except ImportError:
    pass

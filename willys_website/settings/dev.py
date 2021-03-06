from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = True

ALLOWED_HOSTS=['*']

SECRET_KEY = '*z6o_48l9jfhgy6ppuc@yx#ys2s%$aszm%fip-jz*kl-bvnuf5'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BASE_URL = 'http://localhost:8000'

try:
    from .local import *
except ImportError:
    pass

import os

DATA_DIR = '/home/vakkermans/data/fswars/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'fswars.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

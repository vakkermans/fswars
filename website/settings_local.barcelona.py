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

API_KEY = '9cdc313dcbb24d9883503bb4d2341fa1'

COMET_URL = 'http://freesoundwars.com/comet/fswars/cometd'

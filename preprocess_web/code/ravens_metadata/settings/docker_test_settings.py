import os
from os.path import isfile, join
from distutils.util import strtobool

from .local_settings import *

DEBUG = strtobool(os.environ.get('DJANGO_DEBUG', 'False'))

ALLOW_FAB_DELETE = strtobool(os.environ.get('ALLOW_FAB_DELETE', 'False'))

PREPROCESS_DATA_DIR = os.environ.get('PREPROCESS_DATA_DIR', '/raven_metadata')

MEDIA_ROOT_DIRNAME = join(PREPROCESS_DATA_DIR, 'files')
if not isdir(MEDIA_ROOT_DIRNAME):
    os.makedirs(MEDIA_ROOT_DIRNAME)
MEDIA_ROOT = os.environ.get('MEDIA_ROOT',
                            MEDIA_ROOT_DIRNAME)

DATABASE_DIRNAME = join(PREPROCESS_DATA_DIR, 'db')
if not isdir(DATABASE_DIRNAME):
    os.makedirs(DATABASE_DIRNAME)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIRNAME, 'db.sqlite3'),
    }
}

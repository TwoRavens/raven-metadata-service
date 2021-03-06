from __future__ import absolute_import
import json
import sys
import os
from os import makedirs
from os.path import join, normpath, isdir, isfile
from distutils.util import strtobool
import socket

from .base import *

# add cross-origin-resource-sharing header to responses on local dev setup
INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True

ALLOW_FAB_DELETE = True

TIME_ZONE = 'America/New_York'

SECRET_KEY = 'ye-local-laptop-secret-key'

LOCAL_SETUP_DIR = join(dirname(dirname(BASE_DIR)), 'test_setup_local')
if not isdir(LOCAL_SETUP_DIR):
    makedirs(LOCAL_SETUP_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(LOCAL_SETUP_DIR, 'ravens_metadata_01.db3'),
    }
}

SESSION_COOKIE_NAME = 'ravens_metadata_local'

STATIC_URL = '/static/'

#STATICFILES_DIRS = [join(dirname(BASE_DIR), 'static')]

# where static files are collected
STATIC_ROOT = join(LOCAL_SETUP_DIR, 'staticfiles')
if not isdir(STATIC_ROOT):
    makedirs(STATIC_ROOT)

TEST_DIRECT_STATIC = join(dirname(BASE_DIR), 'static')


MEDIA_ROOT = join(LOCAL_SETUP_DIR, 'metadata_files')
if not isdir(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

ALLOWED_HOSTS = ('*', )

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')

PAGE_CACHE_TIME = 0 # No cache in dev

# For local dev, remove some of the user password requirements
#
AUTH_PASSWORD_VALIDATORS = [
    dict(NAME='django.contrib.auth.password_validation.UserAttributeSimilarityValidator'),
    #dict(NAME='django.contrib.auth.password_validation.MinimumLengthValidator'),
    #dict(NAME='django.contrib.auth.password_validation.CommonPasswordValidator'),
    #dict(NAME='django.contrib.auth.password_validation.NumericPasswordValidator'),
]


# -------------------------------
# Set this link if the editor is available
# -------------------------------
# example with preprocess_id 2: http://localhost:1234/2
#
EDITOR_URL = os.environ.get('EDITOR_URL', None) #'http://localhost:1234/')
if not EDITOR_URL:
    EDITOR_URL = None   # Convert an empty string to None

#import logging
#logging.basicConfig(
#        level = logging.DEBUG,
#        format = '%(asctime)s %(levelname)s %(message)s',
#    )

from __future__ import absolute_import
import json
import sys
import os
from os.path import join, normpath, isdir, isfile
from distutils.util import strtobool
import socket

from .local_settings import *

# Adjust the redis connection for docker compose
#REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

#CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)

CELERY_BROKER_URL = 'redis://%s:%d' % (REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://%s:%d' % (REDIS_HOST, REDIS_PORT)

print('-' * 40)
print('CELERY_RESULT_BACKEND', CELERY_RESULT_BACKEND)
print('CELERY_BROKER_URL', CELERY_BROKER_URL)
#CELERY_BROKER_URL = 'redis://localhost'
#CELERY_RESULT_BACKEND = 'redis://localhost'

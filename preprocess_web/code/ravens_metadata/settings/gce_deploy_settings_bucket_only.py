import os, json
from os.path import isfile, join
from distutils.util import strtobool

from .docker_test_settings import *
from google.oauth2 import service_account

# -----------------------------------
# use Google Cloud Storage via django-storages
# -----------------------------------

# add to apps
#
INSTALLED_APPS.append('storages')

# set as default
#
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# bucket name / project id
#
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME',
                                '2ravens-metadata-dev-storage')

GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID',
                               'raven2-186120')

# Credentials from file info
#
creds_info_str = os.environ.get('GCE_CREDS_INFO')
if not creds_info_str:
    print('GCE_CREDS_INFO string NOT FOUND!!!')
    GCE_CREDS_INFO = None
    GS_CREDENTIALS = None
else:
    print('GCE_CREDS_INFO string: %s' % (creds_info_str))
    creds_info_str_decoded = creds_info_str.replace('\n', '')   #.decode("utf-8")
    GCE_CREDS_INFO = json.loads(creds_info_str_decoded)
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(GCE_CREDS_INFO)

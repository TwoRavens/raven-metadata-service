import os
from os.path import abspath, dirname, isfile, join
from .local_settings import *

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

# JSON GCE greds file
#
# reference: https://github.com/jschneier/django-storages/issues/455#issuecomment-380798743
#
dev_creds_file = join(dirname(abspath(__file__)),
                      'gce',
                      'raven2-c6b6c1779dbe.json')
GCE_CREDS_FILE = os.environ.get('GCE_CREDS_FILE',
                                dev_creds_file)
assert isfile(GCE_CREDS_FILE), "GCE creds don't exist: %s" % GCE_CREDS_FILE

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GCE_CREDS_FILE
)

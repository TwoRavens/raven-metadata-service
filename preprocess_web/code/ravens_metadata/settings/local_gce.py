from os.path import abspath, dirname, isfile, join
from .local_settings import *

from google.oauth2 import service_account

INSTALLED_APPS.append('storages')

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_BUCKET_NAME = '2ravens-metadata-dev-storage'

GS_PROJECT_ID = 'raven2-186120'

# reference: https://github.com/jschneier/django-storages/issues/455#issuecomment-380798743
#
CURRENT_SETTINGS_DIR = dirname(abspath(__file__))
GCE_CREDS_FILE = join(CURRENT_SETTINGS_DIR, 'gce', 'raven2-c6b6c1779dbe.json')
assert isfile(GCE_CREDS_FILE), "GCE creds don't exist: %s" % GCE_CREDS_FILE
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GCE_CREDS_FILE
)

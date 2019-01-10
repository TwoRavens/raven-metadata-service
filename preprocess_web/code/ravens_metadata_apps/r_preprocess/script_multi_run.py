"""
script to run multiple r preprocess jobs against the celery queue
"""
import django
import requests
import subprocess
import sys
import os
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)


PROJECT_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
PREPROCESS_DIR = join(PROJECT_DIR, 'preprocess', 'code')
sys.path.append(PREPROCESS_DIR)
PREPROCESS_WEB_DIR = join(PROJECT_DIR, 'preprocess_web', 'code')
sys.path.append(PREPROCESS_WEB_DIR)
#for x in sys.path: print(x)

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ravens_metadata.settings.local_settings')

try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)


def run_jobs():

    for x in range(5):
        pass
    """
    sub = subprocess.Popen(rscript_commands,
                           stdout=subprocess.PIPE)

    preprocess_data = sub.communicate()

    if not preprocess_data:
        error_msg = 'Failed to communicate with preprocess script'
        self.add_err_msg(error_msg)
        return

    try:
        #preprocess_data = preprocess_data[0]
        preprocess_utf8 = preprocess_data[0].decode('utf-8')
    """

def run_one():

    source_file
    url = 'https://httpbin.org/post'
>>> files = {'file': open('report.xls', 'rb')}

>>> r = requests.post(url, files=files)
>>> r.text


if __name__ == '__main__':
    #run_jobs()
    run_one()

"""
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
pj = PreprocessJob.objects.filter(is_success=True).first()
pj.source_file
"""

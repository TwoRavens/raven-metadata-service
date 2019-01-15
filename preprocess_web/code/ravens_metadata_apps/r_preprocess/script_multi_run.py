"""
script to run multiple r preprocess jobs against the celery queue
"""
import django
import requests
from django.urls import reverse
import subprocess
import sys
import os
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)


PROJECT_DIR = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
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
    """Run several R files at once"""
    fnames = ['data_student.tab',
              'fearonLaitin.csv',
              'Census_Judicial_DP_Master_782015.tab',
              'titanic.csv',
              'census-demographics.tab']

    for fname in fnames:
        print('-' * 40)
        print('Process file: ', fname)
        print('-' * 40)
        fpath = join(PROJECT_DIR, 'test_data', fname)
        run_one(fpath)


def run_one(source_file=join(PROJECT_DIR, 'test_data', 'data_student.tab')):
    """run preprocess R"""
    domain = 'http://127.0.0.1:8080'

    url = '%s%s' % (domain, reverse('api_r_preprocess_form'))
    print('url', url)

    #fpath = join(PROJECT_DIR, 'test_data', 'data_student.tab')
    #fpath = join(PROJECT_DIR, 'test_data', 'editor_test.csv')
    files = dict(source_file=open(source_file, 'rb'))

    r = requests.post(url, files=files)

    print(r.text)
    print('status_code', r.status_code)


if __name__ == '__main__':
    run_jobs()
    #run_one()

"""
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
pj = PreprocessJob.objects.filter(is_success=True).first()
pj.source_file
"""

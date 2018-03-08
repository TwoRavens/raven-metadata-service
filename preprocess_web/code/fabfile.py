import os
import shutil
import random
import string
#from os.path import abspath, dirname, join

import signal

import sys
from fabric.api import local, task
import django
#from django.conf import settings
import subprocess

import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
FAB_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FAB_BASE_DIR)

if FAB_BASE_DIR == '/srv/webapps/raven-metadata-service':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'preprocess_service.settings.deploy_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'preprocess_service.settings.local_settings')

try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)



@task
def run_redis():
    """Run the local redis server"""
    redis_cmd = 'redis-server /usr/local/etc/redis.conf'
    local(redis_cmd)


@task
def clear_redis():
    """Clear data from the *running* local redis server"""
    redis_cmd = 'redis-cli flushall  /usr/local/etc/redis.conf'
    local(redis_cmd)

@task
def stop_redis():
    """Clear data from the *running* local redis server"""
    redis_cmd = 'pkill -f redis'
    local(redis_cmd)


@task
def run_celery():
    """Start celery"""
    celery_cmd = ('celery -A ravens_metadata worker -l info')
    local(celery_cmd)

@task
def stop_celery():
    """Stop the celery processes"""
    celery_cmd = ('pkill -f celery')
    local(celery_cmd)

@task
def run_web():
    """Start web server"""
    celery_cmd = ('python manage.py runserver')
    #('cd ravens_metadata;'
    local(celery_cmd)

@task
def clear_jobs():
    """Clear existing jobs. (ONLY ON TEST)"""
    from django.conf import settings
    if not settings.ALLOW_FAB_DELETE:
        print('For testing! Only if ALLOW_FAB_DELETE settings is True')
        return

    from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
    cnt = PreprocessJob.objects.count()
    print('%d PreprocessJob(s) found' % cnt)
    PreprocessJob.objects.all().delete()
    print('Deleted...')

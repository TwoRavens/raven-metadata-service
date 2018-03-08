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
    redis_cmd = 'redis-cli flushall'    #  /usr/local/etc/redis.conf'
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
    init_db()
    run_webserver_cmd = ('python manage.py runserver')
    #('cd ravens_metadata;'
    local(run_webserver_cmd)

@task
def init_db():
    """Run django check and migrate"""
    local("python manage.py check")
    local("python manage.py migrate")
    create_django_superuser()
    create_test_user()
    #local("python manage.py loaddata fixtures/users.json")
    #Series(name_abbreviation="Mass.").save()


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

@task
def create_test_user():
    """Create regular user with creds: test_user/test_user.  No admin access"""
    from tworaven_apps.raven_auth.models import User

    test_username = 'test_user'

    if User.objects.filter(username=test_username).count() > 0:
        print('A "%s" test user already exists' % test_username)
        return

    test_pw = test_username

    new_user = User(username=test_username,
                    first_name='Test',
                    last_name='User',
                    is_staff=False,
                    is_active=True,
                    is_superuser=False)

    new_user.set_password(test_pw)
    new_user.save()

    print('test user created: "%s"' % test_username)
    print('password: "%s"' % test_pw)

@task
def create_test_user():
    """Create regular user with creds: test_user/test_user.  No admin access"""
    from django.contrib.auth.models import User

    test_username = 'test_user'

    if User.objects.filter(username=test_username).count() > 0:
        print('A "%s" test user already exists' % test_username)
        return

    test_pw = test_username

    new_user = User(username=test_username,
                    first_name='Test',
                    last_name='User',
                    is_staff=False,
                    is_active=True,
                    is_superuser=False)

    new_user.set_password(test_pw)
    new_user.save()

    print('test user created: "%s"' % test_username)
    print('password: "%s"' % test_pw)


@task
def create_django_superuser():
    """(Test only) Create superuser with username: dev_admin. Password is printed to the console."""
    from django.contrib.auth.models import User
    #from django.contrib.auth.models import User

    dev_admin_username = 'dev_admin'

    #User.objects.filter(username=dev_admin_username).delete()
    if User.objects.filter(username=dev_admin_username).count() > 0:
        print('A "%s" superuser already exists' % dev_admin_username)
        return

    admin_pw = 'admin'
    #''.join(random.choice(string.ascii_lowercase + string.digits)
    #                   for _ in range(7))

    new_user = User(username=dev_admin_username,
                    first_name='Dev',
                    last_name='Administrator',
                    is_staff=True,
                    is_active=True,
                    is_superuser=True)
    new_user.set_password(admin_pw)
    new_user.save()

    print('superuser created: "%s"' % dev_admin_username)
    print('password: "%s"' % admin_pw)

import os
import shutil
import random
import string
#from os.path import abspath, dirname, join

import signal

import sys
from fabric.api import local, settings, task
import django
#from django.conf import settings
import subprocess

import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
FAB_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FAB_BASE_DIR)

KEY_DJANGO_SETTINGS_MODULE = 'DJANGO_SETTINGS_MODULE'

if not KEY_DJANGO_SETTINGS_MODULE in os.environ:
    if FAB_BASE_DIR == '/var/webapps/raven-metadata-service':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'ravens_metadata.settings.local_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'ravens_metadata.settings.local_settings')

try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)



@task
def redis_run():
    """Run the local redis server"""
    redis_cmd = 'redis-server /usr/local/etc/redis.conf'

    with settings(warn_only=True):
        result = local(redis_cmd, capture=True)

    if result.failed:
        print('Redis may already be running...')


@task
def redis_clear():
    """Clear data from the *running* local redis server"""
    redis_cmd = 'redis-cli flushall'    #  /usr/local/etc/redis.conf'
    with settings(warn_only=True):
        result = local(redis_cmd, capture=True)

    if result.failed:
        print('Redis not running, nothing to clear')

@task
def redis_stop():
    """Clear data from the *running* local redis server"""
    redis_cmd = 'pkill -f redis'
    with settings(warn_only=True):
        result = local(redis_cmd, capture=True)

    if result.failed:
        print('Nothing to stop')

@task
def redis_restart():
    """Stop redis (if it's running) and start it again"""
    redis_stop()
    redis_run()

@task
def celery_run():
    """Clear redis and Start celery"""
    redis_clear()

    celery_cmd = ('celery -A ravens_metadata worker -l info')
    local(celery_cmd)

@task
def celery_stop():
    """Stop the celery processes"""
    celery_cmd = ('pkill -f celery')
    local(celery_cmd)

@task
def celery_restart():
    """Stop celery (if it's running) and start it again"""
    celery_stop()
    celery_run()

@task
def run_shell():
    """Start the django shell"""
    run_shell_cmd = ('python manage.py shell')

    print('run shell: %s' % run_shell_cmd)

    local(run_shell_cmd)

@task
def run_web():
    """Start web server"""
    init_db()
    print('init db complete; start web server')
    run_webserver_cmd = ('python manage.py runserver 8080')

    print('run web server: %s' % run_webserver_cmd)

    local(run_webserver_cmd)

@task
def init_db():
    """Run django check and migrate"""
    print('check settings')
    local("python manage.py check")
    print('update database (if needed)')
    local("python manage.py migrate")
    create_django_superuser()
    create_test_user()
    #local("python manage.py loaddata fixtures/users.json")
    #Series(name_abbreviation="Mass.").save()


@task
def clear_jobs():
    """Delete existing PreprocessJob objects. (ONLY ON TEST)"""
    from django.conf import settings
    if not settings.ALLOW_FAB_DELETE:
        print('For testing! Only if ALLOW_FAB_DELETE settings is True')
        return

    from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
    cnt = PreprocessJob.objects.count()
    print('\n%d PreprocessJob(s) found' % cnt)
    if cnt == 0:
        print('Nothing to delete.')
        return
    PreprocessJob.objects.all().delete()
    print('Deleted...')


@task
def create_test_user():
    """Create regular user with creds: test_user/test_user.  No admin access"""
    from ravens_metadata_apps.raven_auth.models import User

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
    from ravens_metadata_apps.raven_auth.models import User

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

@task
def run_preprocess(input_file, output_file=None):
    """Preprocess a single file. "fab run_preprocess:input_file" or "fab run_preprocess:input_file,output_file" """
    # Bit of a hack here....
    from os.path import dirname, isdir, join
    preprocess_dir = join(dirname(FAB_BASE_DIR),
                          'preprocess',
                          'code')
    #os.chdir(preprocess_dir)

    if output_file:
        preprocess_cmd = 'python3 %s/preprocess.py %s %s' % \
                         (preprocess_dir,
                          input_file,
                          output_file)
    else:
        preprocess_cmd = 'python3 %s/preprocess.py %s' % \
                         (preprocess_dir,
                         input_file)

    print('Run command: "%s"' % preprocess_cmd)
    local(preprocess_cmd)

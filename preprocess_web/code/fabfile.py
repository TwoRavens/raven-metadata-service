import os
import shutil
import random
import string
#from os.path import abspath, dirname, join

import signal
import time

import sys
from fabric import task
import invoke
from invoke import run as fab_local

#from fabric.api import local, settings, task
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
        os.environ.setdefault(KEY_DJANGO_SETTINGS_MODULE,
                              'ravens_metadata.settings.local_settings')
    else:
        os.environ.setdefault(KEY_DJANGO_SETTINGS_MODULE,
                              'ravens_metadata.settings.local_settings')

try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)


def msgt(m):
    print('-' * 40)
    print(m)
    print('-' * 40)

@task
def hello(c):
    print("Hello, world!")

@task
def redis_run(c):
    """Run the local redis server"""
    redis_cmd = 'redis-server /usr/local/etc/redis.conf'

    result = c.run(redis_cmd, warn=True)

    if result.failed:
        msgt('Failed. Redis may already be running')


@task
def redis_clear(c):
    """Clear data from the *running* local redis server"""
    redis_cmd = 'redis-cli flushall'    #  /usr/local/etc/redis.conf'

    result = c.run(redis_cmd)

    if result.failed:
        msgt('Redis (probably) not running, nothing to clear')


@task
def redis_stop(c):
    """Clear data from the *running* local redis server"""
    redis_cmd = 'pkill -f redis'

    result = c.run(redis_cmd, warn=True)

    if result.failed:
        msgt('Redis: Nothing to stop')

@task
def redis_restart(c):
    """Stop redis (if it's running) and start it again"""
    redis_stop(c)
    print('2 second pause')
    time.sleep(2)
    redis_run(c)

@task
def celery_run(c):
    """Clear redis and Start celery"""
    redis_clear(c)

    celery_cmd = ('celery -A ravens_metadata worker -l info')

    result = fab_local(celery_cmd, warn=True)

    if result.failed:
        msgt('celery: failed to run')

@task
def celery_stop(c):
    """Stop the celery processes"""
    celery_cmd = ('pkill -f celery')

    result = fab_local(celery_cmd, warn=True)

    if result.failed:
        msgt('celery: Nothing to stop')

@task
def celery_restart(context):
    """Stop celery (if it's running) and start it again"""
    celery_stop(context)
    celery_run(context)

@task
def run_shell(c):
    """Start the django shell"""
    run_shell_cmd = ('python manage.py shell')

    print('run shell: %s' % run_shell_cmd)

    result = fab_local(run_shell_cmd, warn=True)

    if result.failed:
        msgt('django shell: failed to run')

@task
def run_web(context):
    """Start django dev server"""
    init_db(context)

    print('init db complete; start web server')
    run_webserver_cmd = ('python manage.py runserver 8080')

    print('run web server: %s' % run_webserver_cmd)
    fab_local(run_webserver_cmd)

@task
def init_db(context):
    """Run django check and migrate"""
    print('check settings')
    fab_local("python manage.py check")

    print('update database (if needed)')
    fab_local("python manage.py migrate")


    print('create users...')
    create_django_superuser(context)
    create_test_user(context)
    load_registered_dataverses(context)
    load_latest_schema(context)
    #local("python manage.py loaddata fixtures/users.json")
    #Series(name_abbreviation="Mass.").save()

@task
def load_registered_dataverses(context):
    """If none exist, load RegisteredDataverse objects from fixtures"""
    from ravens_metadata_apps.dataverse_connect.models import RegisteredDataverse

    cnt = RegisteredDataverse.objects.count()
    if cnt > 0:
        print('RegisteredDataverse object(s) already exist: %s' % cnt)
        return

    load_cmd = ('python manage.py loaddata ravens_metadata_apps/dataverse_connect'
                '/fixtures/initial_fixtures.json')
    fab_local(load_cmd)

@task
def load_latest_schema(context):
    """Make sure the schema is loaded to the database; Load one if needed."""
    from ravens_metadata_apps.metadata_schemas.models import MetadataSchema
    from ravens_metadata_apps.metadata_schemas.schema_util import SchemaUtil

    schema_info = SchemaUtil.get_latest_schema()
    if schema_info.success:
        mschema = schema_info.result_obj
        if mschema:
            print('MetadataSchema exists')
            return


    load_cmd = ('python manage.py loaddata ravens_metadata_apps/metadata_schemas'
                '/fixtures/initial_001.json')
    fab_local(load_cmd)
    print('Default MetadataSchema loaded')




@task
def collectstatic(context):
    """Run the Django collectstatic command"""
    fab_local('python manage.py collectstatic --noinput')

@task
def clear_metadata_updates(context):
    """Delete all MetadataUpdate objects"""
    from django.conf import settings
    if not settings.ALLOW_FAB_DELETE:
        print('For testing! Only if ALLOW_FAB_DELETE settings is True')
        return

    from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob, MetadataUpdate

    mcnt = MetadataUpdate.objects.count()
    print('\n%d MetadataUpdate(s) found' % mcnt)
    if mcnt > 0:
        for meta_obj in MetadataUpdate.objects.all().order_by('-id'):
            if meta_obj.metadata_file:
                meta_obj.metadata_file.delete()
            meta_obj.delete()
        print('Deleted...')
    else:
        print('No MetadataUpdate objects found.\n')

@task
def clear_jobs(context):
    """Delete existing PreprocessJob objects. (ONLY ON TEST)"""
    from django.conf import settings
    if not settings.ALLOW_FAB_DELETE:
        print('For testing! Only if ALLOW_FAB_DELETE settings is True')
        return

    from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob, MetadataUpdate

    mcnt = MetadataUpdate.objects.count()
    print('\n%d MetadataUpdate(s) found' % mcnt)
    if mcnt > 0:
        for meta_obj in MetadataUpdate.objects.all().order_by('-id'):
            if meta_obj.metadata_file:
                meta_obj.metadata_file.delete()
            meta_obj.delete()
        print('Deleted...')
    else:
        print('No MetadataUpdate objects found.\n')

    cnt = PreprocessJob.objects.count()
    print('\n%d PreprocessJob(s) found' % cnt)
    if cnt == 0:
        print('No PreprocessJob objects found.\n')
        return
    for job in PreprocessJob.objects.all():
        if job.source_file:
            job.source_file.delete()

        if job.metadata_file:
            job.metadata_file.delete()
        job.delete()
    print('Deleted...')


@task
def create_test_user(context):
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
def create_django_superuser(context):
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
def run_preprocess(context, input_file, output_file=None):
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
    fab_local(preprocess_cmd)

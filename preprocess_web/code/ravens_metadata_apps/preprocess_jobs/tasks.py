"""
Simple test for celery to run preprocess tasks
"""
from __future__ import absolute_import, unicode_literals

import sys
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)

# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'preprocess',
                      'code')
sys.path.append(PREPROCESS_DIR)

from datetime import datetime
import time
from celery import Celery, shared_task
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase


from preprocess_runner import PreprocessRunner
from msg_util import msg, msgt

from celery import task, shared_task

from ravens_metadata.celery import celery_app



@shared_task
def preprocess_csv_file(input_file, **kwargs):
    """Run preprocess on a csv file"""
    init_timestamp = datetime.now()
    start_time = time.time()
    job_id = kwargs.get('job_id')

    print('(%s) Start preprocess: %s' % (init_timestamp, input_file))

    # Split out the filename and extension
    # - check if it's tab delimited
    #
    fname_base, fname_ext = splitext(basename(input_file))
    if fname_ext.lower() == '.tab':
        runner, user_msg = PreprocessRunner.load_from_tabular_file(\
                                    input_file, job_id=job_id)
    else:
        runner, user_msg = PreprocessRunner.load_from_csv_file(input_file, job_id=job_id)

    if user_msg:
        print('(%s) FAILED: %s' % (input_file, user_msg))
        return dict(success=False,
                    input_file=input_file,
                    message=user_msg)

    #runner.show_final_info()

    # ------------------------------
    # prepare final JSON output and
    # write to file
    # ------------------------------
    jstring = runner.get_final_json(indent=4)

    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    return dict(success=True,
                input_file=input_file,
                message=user_msg,
                elapsed_time=elapsed_time_str,
                data=runner.get_final_dict())


@shared_task
def xpreprocess_csv_file(input_file, output_dir=None):
    """Run preprocess on a csv file"""
    init_timestamp = datetime.now()
    start_time = time.time()

    print('(%s) Start preprocess: %s' % (init_timestamp, input_file))

    if output_dir is not None and isdir(output_dir):
        return dict(success=False,
                    input_file=input_file,
                    message='Directory does not exist: %s' % output_dir)

    # Split out the filename and extension
    # - check if it's tab delimited
    #
    fname_base, fname_ext = splitext(basename(input_file))
    if fname_ext.lower() == '.tab':
        runner, user_msg = PreprocessRunner.load_from_tabular_file(\
                                    input_file)
    else:
        runner, user_msg = PreprocessRunner.load_from_csv_file(input_file)

    if user_msg:
        print('(%s) FAILED: %s' % (input_file, user_msg))
        return dict(success=False,
                    input_file=input_file,
                    message=user_msg)

    #runner.show_final_info()

    # ------------------------------
    # prepare final JSON output and
    # write to file
    # ------------------------------
    jstring = runner.get_final_json(indent=4)

    if output_dir is None:
        # your script
        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        return dict(success=True,
                    input_file=input_file,
                    message=user_msg,
                    elapsed_time=elapsed_time_str,
                    data=runner.get_final_dict())

    # create output filename
    output_filepath = None
    for _idx in range(5):
        output_filepath = '%s_%s.json' % \
                          (fname_base, get_alphanumeric_lowercase(5))
        output_filepath = join(output_dir, output_filepath)
        if not isfile(output_filepath):
            break

    if isfile(output_filepath):
        user_msg = 'Output file already exists (tried 5 random names): %s' % \
                    (output_filepath)
        print('%s FAILED: %s' % (input_file, user_msg))
        return dict(success=False,
                    input_file=input_file,
                    message=user_msg)

    try:
        open(output_filepath, 'w').write(jstring)
    except OSError as os_err:
        user_msg = 'Failed to write file: %s' % (os_err)
        print('(%s) FAILED: %s' % (input_file, user_msg))
        return dict(success=False,
                    input_file=input_file,
                    message=user_msg)

    user_msg = 'file written: %s' % output_filepath
    print('(%s) SUCCESS: %s' % (init_timestamp, user_msg))

    # your script
    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    print('   - elapsed time: %s' % (elapsed_time_str))


    return dict(success=True,
                input_file=input_file,
                message=user_msg,
                elapsed_time=elapsed_time_str,
                data=runner.get_final_dict())
                #data=runner.get_final_dict())

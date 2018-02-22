"""
Simple test for celery to run preprocess tasks
"""
import sys
import time
import json
from os.path import \
    (abspath, basename, dirname, isdir, join, splitext)
from celery import Celery

import logging

# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'preprocess',
                      'code')
sys.path.append(PREPROCESS_DIR)
from preprocess_runner import PreprocessRunner
from msg_util import msg, msgt

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


BROKER_URL = 'redis://localhost'

app = Celery('basic_preprocess',
             backend=BROKER_URL,
             broker=BROKER_URL)

TASK_NUM = 0
@app.task
def preprocess_csv_file(input_file, output_dir):
    """Run preprocess on a csv file"""
    global TASK_NUM
    TASK_NUM += 1
    print('(%d) Start preprocess: %s' % (TASK_NUM, input_file))
    if not isdir(output_dir):
        return dict(success=False,
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
        print('(%d) FAILED: %s' % (TASK_NUM, user_msg))
        return dict(success=False,
                    message=user_msg)


    #runner.show_final_info()

    # ------------------------------
    # prepare final JSON output and
    # write to file
    # ------------------------------
    jstring = runner.get_final_json(indent=4)
    output_filepath = join(output_dir, '%s.json' % fname_base)

    try:
        open(output_filepath, 'w').write(jstring)
    except OSError as os_err:
        user_msg = 'Failed to write file: %s' % (os_err)
        print('(%d) FAILED: %s' % (TASK_NUM, user_msg))
        return dict(success=False,
                    message=user_msg)

    user_msg = 'file written: %s' % output_filepath
    print('(%d) SUCCESS: %s' % (TASK_NUM, user_msg))

    return dict(success=True,
                message=user_msg,
                data=runner.get_final_json())
                #data=runner.get_final_dict())

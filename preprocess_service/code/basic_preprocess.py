"""
Simple test for celery to run preprocess tasks
"""
import sys
from datetime import datetime
import time
import json
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)
import logging

from celery import Celery
from random_util import get_alphanumeric_lowercase

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


@app.task
def preprocess_csv_file(input_file, output_dir=None):
    """Run preprocess on a csv file"""
    init_timestamp = datetime.now()
    start_time = time.time()

    print('(%s) Start preprocess: %s' % (init_timestamp, input_file))
    if output_dir and not isdir(output_dir):
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

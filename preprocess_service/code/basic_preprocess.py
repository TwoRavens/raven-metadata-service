"""
Simple test for celery to run preprocess tasks
"""
import sys
import time
import json
from os.path import \
    (abspath, basename, dirname, isdir, join, splitext)
from celery import Celery
# Register your new serializer methods into kombu
from kombu.serialization import register

# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'preprocess',
                      'code')
sys.path.append(PREPROCESS_DIR)
from preprocess_runner import PreprocessRunner
from np_json_encoder import NumpyJSONEncoder, np_dumps
from msg_util import msg, msgt

register('pjson', np_dumps, json.loads,
         content_type='application/pjson',
         content_encoding='utf-8')

BROKER_URL = 'redis://localhost'

app = Celery('basic_preprocess',
             result_serializer='pjson',
             task_serializer='pjson',
             backend=BROKER_URL,
             broker=BROKER_URL)

@app.task
def preprocess_csv_file(input_file, output_dir):
    """Run preprocess on a csv file"""
    if not isdir(output_dir):
        return dict(success=False,
                    message='Directory does not exist: %s' % output_dir)

    # Split out the filename and extension
    # - check if it's tab delimited
    #
    fname_base, fname_ext = splitext(basename(input_file))
    #print('fname_base', fname_base)
    #print('fname_ext', fname_ext)
    if fname_ext.lower() == '.tab':
        runner, user_msg = PreprocessRunner.load_from_tabular_file(\
                                    input_file)
    else:
        runner, user_msg = PreprocessRunner.load_from_csv_file(input_file)

    if user_msg:
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
        return dict(success=False,
                    message=user_msg)

    user_msg = 'file written: %s' % output_filepath
    return dict(success=True,
                message=user_msg,
                data=runner.get_final_json())
                #data=runner.get_final_dict())

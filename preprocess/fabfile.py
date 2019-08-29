import os
import random
import string
import sys
from fabric import task
from invoke import run as fab_local

# ----------------------------------------------------
# Add this directory to the python system path
# ----------------------------------------------------
FAB_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(FAB_BASE_DIR)

@task
def run_preprocess(context, input_file, output_file=None):
    """Preprocess a single file. "fab run_preprocess:input_file" or "fab run_preprocess:input_file,output_file" """
    # Bit of a hack here....
    from os.path import dirname, isdir, join
    preprocess_dir = join(FAB_BASE_DIR,
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

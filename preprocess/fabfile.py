from os.path import abspath, dirname, isdir, join
from fabric import task
from invoke import run as fab_local

CURRENT_DIR = dirname(abspath(__file__))

@task
def run_preprocess(c, input_file, output_file=None):
    """Preprocess a single file. "fab run_preprocess:input_file" or "fab run_preprocess:input_file,output_file" """
    preprocess_dir = join(CURRENT_DIR, 'raven_preprocess')

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

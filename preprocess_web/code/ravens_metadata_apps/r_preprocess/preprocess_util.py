"""
Run the preprocess job
"""
import sys
import subprocess

from os.path import isfile, join, normpath
import json

from django.conf import settings

from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.preprocess_jobs.job_util import \
    (JobUtil,)


def run_preprocess(job_id):
    """Run as a script for now...to get things going"""

    job_info = JobUtil.get_preprocess_job_object(job_id)
    if not job_info.success:
        return job_info

    job = job_info.result_obj

    print(job.source_file_path())

    filepath = job.source_file_path()
    run_r_preprocess(filepath)



def parse_preprocess_output(pout):
    """Parse output for preprocess JSON"""
    phrase = '---START-PREPROCESS-JSON---'
    idx = pout.find(phrase)
    if idx == -1:
        print('Output not found!')
        return err_resp('output not found ("%s")' % phrase)

    end_phrase = '---STOP-PREPROCESS-JSON---'
    end_idx = pout.find(end_phrase, idx+len(phrase))
    if end_idx == -1:
        print('Not found!')
        return err_resp('output not found ("%s")' % end_phrase)


    print('got it')
    pout_formatted = pout[idx+len(phrase):end_idx]

    #line1_fmt = '[1] "'
    #pout_formatted = pout_formatted.replace(line1_fmt, '')

    return ok_resp(pout_formatted)

def run_r_preprocess(filename):
    """Run the R script"""
    if not isfile(filename):
        print('File not found: %s' % filename)
        return

    print('-' * 40)
    print('settings.BASE_DIR', settings.BASE_DIR)
    print('-' * 40)

    script_dir = normpath(join(\
                    settings.BASE_DIR,
                    '..',
                    'ravens_metadata_apps',
                    'r_preprocess',
                    'rscripts'))

    script_path = join(script_dir, 'runPreprocess.R')

    print('script_path', script_path)
    print('-' * 40)
    rscript_cmds = ['/usr/local/bin/rscript',
                    script_path,
                    filename,
                    script_dir]

    print('rscript_cmd', rscript_cmds)
    print('-' * 40)

    sub = subprocess.Popen(rscript_cmds,
                           stdout=subprocess.PIPE)

    preprocess_data = sub.communicate()
    if not preprocess_data:
        print('-' * 40)
        print('failed to communicate with preprocess script')
        return

    #output_info = parse_preprocess_output(sub.out)
    output_info = parse_preprocess_output(preprocess_data[0].decode('utf-8'))
    if not output_info.success:
        print('-' * 40)
        print(output_info.err_msg)
        print('-' * 40)
        return

    metadata = output_info.result_obj.strip()
    print('-' * 40)
    print(metadata)
    print('-' * 40)

    m2 = json.loads(metadata)
    print(json.dumps(m2, indent=4))

"""
from subprocess import Popen, PIPE
cmd = ['/usr/local/bin/rscript', '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_web/code/ravens_metadata_apps/r_preprocess/rscripts/runPreprocess.R', '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_web/test_setup_local/metadata_files/source_file/2019/01/07/editor_test_L2TY8Tz.csv']
p = subprocess.Popen(cmd, stdout=PIPE)
msg = p.communicate()[0]
"""

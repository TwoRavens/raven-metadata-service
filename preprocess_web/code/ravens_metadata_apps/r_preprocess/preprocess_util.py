"""
Run the R preprocess script
NOTE: The "preprocess.R" script is located at the top of this repository
    - /rsripts/preprocess.R
    - /rsripts/runPreprocess.R  # wrapper for preprocess.R
"""
import logging
import sys
import subprocess
import time

from os.path import isdir, isfile, join, normpath
import json

from django.conf import settings

from ravens_metadata_apps.utils.basic_err_check import \
    (BasicErrCheck,)
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.utils.json_util import \
    (json_loads,)
from ravens_metadata_apps.preprocess_jobs.job_util import \
    (JobUtil,)
from ravens_metadata_apps.preprocess_jobs.preprocess_result_updater import \
    (PreprocessResultUpdater)

LOGGER = logging.getLogger(__name__)

class PreprocessUtil(BasicErrCheck):
    """For running R preprocess"""
    START_PREPROCESS_MARKER = '---START-PREPROCESS-JSON---'
    END_PREPROCESS_MARKER = '---END-PREPROCESS-JSON---'

    def __init__(self, job_id):
        """Start with a job_id"""
        self.job_id = job_id
        self.job_obj = None

        self.start_time = time.time()

        # Right now this isn't working for AWS S3, Google Buckets
        self.source_file_path = None

        self.run_steps()


    def add_err_msg(self, err_msg):
        """Add an error message and save the result"""
        print('add_err_msg', err_msg)
        # ---------------------------------
        #  basic method
        # ---------------------------------
        super(PreprocessUtil, self).add_err_msg(err_msg)


        # ---------------------------------
        # save this to the preprocess job
        # ---------------------------------
        result_info = dict(success=False,
                           job_id=self.job_id,
                           user_message=err_msg)

        if self.job_obj:
            result_info['input_file'] = self.job_obj.source_file

        updater = PreprocessResultUpdater(**result_info)

        if updater.has_error():
            print(updater.get_error_message())


    def run_steps(self):
        """Run Preprocss R on a file"""
        if self.has_error():
            return

        self.step_10_retrieve_job()
        if self.has_error():
            return

        rscript_commands = self.step_20_get_script_commands()
        if not rscript_commands:
            return

        self.step_30_run_preprocess_script(rscript_commands)


    def step_10_retrieve_job(self):
        """Retrieve the Preprocess Job object"""
        LOGGER.debug('step_10_retrieve_job')
        if self.has_error():
            return

        if not self.job_id:
            self.add_err_msg('The "job_id" must be set!')
            return

        # Get the PreprocessJob
        #
        job_info = JobUtil.get_preprocess_job_object(self.job_id)
        if not job_info.success:
            self.add_err_msg(job_info.err_msg)
            return

        self.job_obj = job_info.result_obj

        # Check for the source file path
        #
        filepath_info = self.job_obj.source_file_path()
        if not filepath_info.success:
            self.add_err_msg(filepath_info.err_msg)
            return

        self.source_file_path = filepath_info.result_obj

    def step_20_get_script_commands(self):
        """Run R Preprocess via python subprocess"""
        LOGGER.debug('step_20_get_script_commands')

        if self.has_error():
            return None

        # ------------------------------------
        #   Make sure file exists
        # ------------------------------------
        if not isfile(self.source_file_path):
            self.add_err_msg('File not found: %s' % self.source_file_path)
            return None

        # ------------------------------------
        # Set full paths for "rscript" command
        # and R preprocess
        # ------------------------------------
        r_script_directory = normpath(join(\
                                settings.BASE_DIR,
                                '..',
                                '..',
                                '..',
                                #'ravens_metadata_apps',
                                #'r_preprocess',
                                'rscripts'))

        if not isdir(r_script_directory):
            self.add_err_msg(('R script directory not'
                              ' found: %s' % r_script_directory))
            return None

        script_path = join(r_script_directory, 'runPreprocess.R')
        if not isfile(script_path):
            self.add_err_msg(('preprocess R script not'
                              ' found: %s' % script_path))
            return None

        rscript_cmds = [settings.R_SCRIPT_PATH,
                        script_path,
                        self.source_file_path,
                        r_script_directory]

        return rscript_cmds


    def step_30_run_preprocess_script(self, rscript_commands):
        """Run R script"""
        LOGGER.debug('step_30_run_preprocess_script: %s', rscript_commands)

        if self.has_error():
            return

        LOGGER.debug('-' * 40)

        sub = subprocess.Popen(rscript_commands,
                               stdout=subprocess.PIPE)

        preprocess_data = sub.communicate()

        if not preprocess_data:
            error_msg = 'Failed to communicate with preprocess script'
            self.add_err_msg(error_msg)
            return

        try:
            #preprocess_data = preprocess_data[0]
            preprocess_utf8 = preprocess_data[0].decode('utf-8')
        except IndexError as err_resp:
            self.add_err_msg(('Failed to retrieve preprocess'
                              ' data. %s') % err_resp)
            return

        LOGGER.debug('(2) preprocess_data %s', preprocess_utf8)
        LOGGER.debug('-' * 40)

        output_info = self.parse_preprocess_output(preprocess_utf8)
        if not output_info.success:
            self.add_err_msg('Failed to parse preprocess response. %s' \
                             % output_info.err_msg)
            return

        metadata = output_info.result_obj.strip()

        # ---------------------------------------------
        # Convert the JSON string to a python dict
        # ---------------------------------------------
        final_dict_info = json_loads(metadata)
        if not final_dict_info.success:
            self.add_err_msg('Failed to convert metadata to JSON. %s' \
                             % final_dict_info.err_msg)
            return


        # ---------------------------------------------
        # Save the result to the database
        # ---------------------------------------------
        result_info = dict(success=True,
                           job_id=self.job_id,
                           input_file=self.job_obj.source_file,
                           user_message="File processed.",
                           elapsed_time=self.get_elapsed_time_str(),
                           data=final_dict_info.result_obj)

        updater = PreprocessResultUpdater(**result_info)
        if updater.has_error():
            self.add_err_msg('Failed to save metadata. %s' \
                             % updater.get_error_message())



    def get_elapsed_time_str(self):
        """Return the elapsed time in string format"""
        elapsed_time = time.time() - self.start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        return elapsed_time_str

    def parse_preprocess_output(self, preprocess_output):
        """Parse output for preprocess JSON"""
        if not preprocess_output:
            return err_resp('preprocess_output must be set')

        idx = preprocess_output.find(self.START_PREPROCESS_MARKER)
        if idx == -1:
            print('Output not found!')
            return err_resp('output not found ("%s")' % self.START_PREPROCESS_MARKER)

        idx_end_start_phrase = idx+len(self.START_PREPROCESS_MARKER)

        end_idx = preprocess_output.find(self.END_PREPROCESS_MARKER,
                                         idx_end_start_phrase)
        if end_idx == -1:
            user_msg = 'output not found ("%s")' % \
                        self.END_PREPROCESS_MARKER
            return err_resp(user_msg)

        preprocess_output = preprocess_output[idx_end_start_phrase:end_idx]

        return ok_resp(preprocess_output)

"""
from subprocess import Popen, PIPE
cmd = ['/usr/local/bin/rscript', '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_web/code/ravens_metadata_apps/r_preprocess/rscripts/runPreprocess.R', '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_web/test_setup_local/metadata_files/source_file/2019/01/07/editor_test_L2TY8Tz.csv']
p = subprocess.Popen(cmd, stdout=PIPE)
msg = p.communicate()[0]
"""

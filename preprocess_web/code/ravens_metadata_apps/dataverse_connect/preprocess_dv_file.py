import os, sys
import csv
from os.path import abspath, dirname, join

code_dir1 = dirname(dirname(dirname(abspath(__file__))))
code_dir2 = join(dirname(dirname(code_dir1)), 'preprocss', 'code')
sys.path.extend([code_dir1, code_dir2])

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ravens_metadata.settings.local_settings')

import django
try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)

from ravens_metadata_apps.dataverse_connect.dataverse_file_retriever import \
    (DataverseFileRetriever)
from ravens_metadata_apps.dataverse_connect.tasks import preprocess_dataverse_file
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.dataverse_connect.dataverse_util import DataverseUtil
from msg_util import msg, msgt


def try_it(file_id=3147445, dataset_id=None):

    # hmmm...
    # https://dataverse.harvard.edu/file.xhtml?fileId=3147445&datasetVersionId=136558
    dv_url = 'https://dataverse.harvard.edu/api/access/datafile/%s' % file_id
    file_retriever = DataverseFileRetriever(dv_url, dataset_id=dataset_id)
    if file_retriever.has_error():
        print('error found: %s' % file_retriever.get_error_message())
        return

    print(file_retriever.preprocess_job)

    JobUtil.start_preprocess(file_retriever.preprocess_job)


def try_queue(file_id=3147445, dataset_id=None):

    # hmmm...
    # https://dataverse.harvard.edu/file.xhtml?fileId=3147445&datasetVersionId=136558
    dv_url = 'https://dataverse.harvard.edu/api/access/datafile/%s' % file_id

    job_info = DataverseUtil.process_dataverse_file(dv_url, dataset_id=dataset_id)
    if job_info.success:
        print('it worked!!')
        print('job: %s' % job_info.result_obj)
    else:
        print('failed!')
        print(job_info.err_msg)
    #preprocess_dataverse_file.delay(dv_url, dataset_id=dataset_id)


def try_it2():

    tab_file_list = '/Users/ramanprasad/Google Drive/2Ravens/dv_data/tabular_2017_00829.csv'
    cnt = 0

    with open(tab_file_list, "r") as f:
        reader = csv.reader(f)
        for idx, line_items in enumerate(reader):
            if idx < 1000:
                continue
            #line_items = line.split(',')
            print('line_items', line_items)
            file_id = line_items[0]
            dataset_id = line_items[1]
            filesize = line_items[3]
            if str(file_id).isdigit() and int(filesize) < 1800000:
                cnt += 1
                msgt('(%s) Process file: %s (idx: %s)' % (cnt, file_id, idx))
                #try_queue(3148839, dataset_id)
                try_queue(file_id, dataset_id)
            if cnt == 120:
                break

if __name__ == '__main__':
    #try_queue(3131016)

    #try_it(3131016)
    try_it2()
    #try_queue()

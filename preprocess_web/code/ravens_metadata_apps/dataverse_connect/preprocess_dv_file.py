import os, sys
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
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil


def try_it(file_id=3147445):
    # hmmm...
    # https://dataverse.harvard.edu/file.xhtml?fileId=3147445&datasetVersionId=136558
    dv_url = 'https://dataverse.harvard.edu/api/access/datafile/%s' % file_id

    file_retriever = DataverseFileRetriever(dv_url)
    if file_retriever.has_error():
        print('error found: %s' % file_retriever.get_error_message())
        return

    print(file_retriever.preprocess_job)

    JobUtil.start_preprocess(file_retriever.preprocess_job)


if __name__ == '__main__':
    try_it()

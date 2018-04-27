from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)

import pandas as pd

pid = 21

job = PreprocessJob.objects.get(pk=21)

df = pd.read_csv(job.source_file.path)

start_row = 1
nrows = 10
df = pd.read_csv(job.source_file.path,
                 skiprows=start_row,
                 # skip rows range starts from 1 as 0 row is the header
                 nrows=nrows)

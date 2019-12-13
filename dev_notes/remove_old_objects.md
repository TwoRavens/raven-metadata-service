

```

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from google.api_core.exceptions import NotFound
l = PreprocessJob.objects.filter(name='datamart_temp.csv')
import time

def del_jobs(job_list):
  cnt = 0
  for p in job_list:
    cnt += 1
    print(f'{cnt} delete {p}')
    if p.source_file:
      try:
        p.source_file.delete()
        print('  source_file deleted...')
      except NotFound:
        print('no source file...')

    if p.metadata_file:
      try:
        p.metadata_file.delete()
        print('  metadata_file deleted...')
      except NotFound:
        print('no metadata_file...')
    if p.id:
      p.delete()
      print('  deleted...')
    print('sleep...')
    time.sleep(.25)

params = dict(name__endswith='0000.csv')
l = PreprocessJob.objects.filter(**params); l.count()


del_jobs(l)

```

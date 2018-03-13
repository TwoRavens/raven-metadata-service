import django
import sys
import os
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)


CURRENT_DIR = dirname(abspath(__file__))
PREPROCESS_DIR = join(dirname(dirname(CURRENT_DIR)), 'preprocess', 'code')
sys.path.append(PREPROCESS_DIR)
PREPROCESS_WEB_DIR = join(dirname(dirname(CURRENT_DIR)), 'preprocess_web', 'code')
sys.path.append(PREPROCESS_WEB_DIR)
for x in sys.path: print(x)

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ravens_metadata.settings.local_settings')

try:
    django.setup()
except Exception as e:
    print("WARNING: Can't configure Django. %s" % e)

# ------------------------------------------------------------

# ------------------------------------------------------------
from django import template

from django.template.loader import render_to_string
from column_info import ColumnInfo

column_info = ColumnInfo('someVar')

template_file = join(CURRENT_DIR, 'single_var.rst')
ze_template = template.Template(open(template_file, 'r').read())

attr_keys = column_info.__dict__.keys()
doc_list = []
for attr in attr_keys:
    info = dict(var_name=attr)
    var_doc = ze_template.render(template.Context((info)))
    doc_list.append(var_doc)

print ('\n'.join(doc_list[:2]))

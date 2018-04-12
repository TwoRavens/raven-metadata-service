from os.path import isfile
from collections import OrderedDict
import json

def get_preprocess_filename(preprocess_id, version=None):
    """Return a filename used for a preprocess download"""
    assert preprocess_id, "preprocess_id cannot be None"
    assert str(preprocess_id).isdigit(), "preprocess_id must be numeric"

    if not version:
        version = '1.0'

    version = str(version).replace('.', '-')

    fname = 'preprocess_%s_v%s.json' % (preprocess_id, version)

    return fname

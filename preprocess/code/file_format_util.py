import pandas as pd
import json,collections


class FileFormatUtil(object):
    def __init__(self,frame):
        """Identify file type: csv, tab, etc"""


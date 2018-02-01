
import unittest

import json
import sys
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile

CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))


class MyTest(unittest.TestCase):
    def test_nulls(self):
        pass
        # create dataframe

        # import type guess class

        # make type

        #self.assertEqual(fun(3), 4)

from __future__ import absolute_import
import json
import sys
import os
from os.path import join, normpath, isdir, isfile
from distutils.util import strtobool
import socket

from .local_settings import *

ALLOW_FAB_DELETE = False

MEDIA_ROOT = '/tmp'

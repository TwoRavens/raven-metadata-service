from collections import OrderedDict
import decimal
import json, time, datetime
import pandas as pd
import os
from os.path import isdir, isfile
from preprocess_runner import*

from msg_util import msg, msgt

# Move these elsewhere as things progress ....
# ---------------------------------------------
CSV_FILE_EXT = '.csv'
TAB_FILE_EXT = '.tab'
ACCEPTABLE_FILE_TYPE_EXTS = \
                    (CSV_FILE_EXT,
                     TAB_FILE_EXT)
ACCEPTABLE_EXT_LIST = ', '.join(['"%s"' % x for x in ACCEPTABLE_FILE_TYPE_EXTS])
# ---------------------------------------------


class FileFormatUtil(object):
    def __init__(self,file,**kwargs):
        """Identify file type: csv, tab, etc"""
        print("The file format class is called")
        self.input_file = file
        self.job_id = kwargs.get('job_id')
        self.fname = kwargs.get('fname')
        self.fname_ext = kwargs.get('fname_ext')
        self.fname_ext_check = self.fname_ext.lower()
        self.check_file()


    def check_file(self):
        """ handels all the files"""
        if not isfile(self.input_file):
            return None, 'The file was not found: [%s]' % self.input_file

        filesize = os.stat(self.input_file).st_size
        if filesize == 0:
            return None, 'The file size is zero: [%s]' % self.input_file
        else:
            self.set_format_etc()


    def set_format_etc(self):
        """ here it checks the format and set"""
        if self.fname_ext_check == TAB_FILE_EXT:
            runner, err_msg = self.get_dataframe(TAB_FILE_EXT);
            return runner, err_msg
        elif self.fname_ext_check == CSV_FILE_EXT:
            runner, err_msg = self.get_dataframe(CSV_FILE_EXT);
            return runner, err_msg
        else:
            err_msg = ('We currently do not process this file type.'
                       ' Please use a file with one of the following'
                       ' extensions: %s') % \
                      (ACCEPTABLE_EXT_LIST,)
            runner = None
            return runner, err_msg


        # ## database
        # - database -> dataframe
        # - type: mysql
        #
        # ## apache ray type of thing
        # - in -memory -> dataframe

    def get_dataframe(self, format):
        """ get dataframe on basis of the format"""
        if format == TAB_FILE_EXT:
         try:
            df = pd.read_csv(self.input_file,
                             delimiter='\t')
         except pd.errors.ParserError as err_obj:
            err_msg = ('Failed to load csv file (pandas ParserError).'
                       ' \n - File: %s\n - %s') % \
                      (self.input_file, err_obj)
            return None, err_msg
         except PermissionError as err_obj:
            err_msg = ('No read prermission on this file:'
                       ' \n - File: %s\n - %s') % \
                      (self.input_file, err_obj)
            return None, err_msg
         except Exception as err_obj:
            err_msg = ('Failed to load csv file.'
                       ' \n - File: %s\n - %s') % \
                      (self.input_file, err_obj)
            return None, err_msg
         print("*******df********", df)
         return df,None

        if format == CSV_FILE_EXT:
            try:
                df = pd.read_csv(self.input_file,
                             delimiter=None)
            except pd.errors.ParserError as err_obj:
                err_msg = ('Failed to load csv file (pandas ParserError).'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                return None, err_msg
            except PermissionError as err_obj:
                err_msg = ('No read prermission on this file:'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                return None, err_msg
            except Exception as err_obj:
                err_msg = ('Failed to load csv file.'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                return None, err_msg
            print("*******df********",df)
            return df,None






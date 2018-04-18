from collections import OrderedDict
import decimal
import json, time, datetime
import pandas as pd
import os
from os.path import isdir, isfile
from preprocess_runner import*
from data_source_util import DataSourceUtil
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
        # print("The file format class is called")
        self.input_file = file
        self.job_id = kwargs.get('job_id')

        self.fname_ext = kwargs.get('fname_ext')
        self.fname_ext_check = self.fname_ext.lower()

        self.dataframe = None
        self.data_source_info = None # instance of DataSourceInfo

        # data source info
        self.fname = kwargs.get('fname')
        self.type = None
        self.format = None

        #
        self.has_error = False
        self.error_message = None


        self.check_file()

    def add_error(self,err):
        self.has_error = True
        self.error_message = err

    def check_file(self):
        """ handels all the files"""
        if not isfile(self.input_file):
            self.add_error('The file was not found: [%s]' % self.input_file)

            return None, self.error_message

        filesize = os.stat(self.input_file).st_size
        if filesize == 0:
            self.add_error('The file size is zero: [%s]' % self.input_file)
            return None, self.error_message
        else:
            self.set_format_etc()


    def set_format_etc(self):
        """ here it checks the format and set"""
        if self.fname_ext_check == TAB_FILE_EXT:
            runner = self.get_dataframe(TAB_FILE_EXT)
            self.type = "File"
            self.format = TAB_FILE_EXT
            data_source_info_object = DataSourceUtil(name=self.fname, type= self.type, format= self.format)
            if not data_source_info_object.has_error:
                self.data_source_info = data_source_info_object.output


        elif self.fname_ext_check == CSV_FILE_EXT:
            runner = self.get_dataframe(CSV_FILE_EXT)
            self.type = "File"
            self.format = CSV_FILE_EXT
            data_source_info_object = DataSourceUtil(name=self.fname, type=self.type, format=self.format)
            if not data_source_info_object.has_error:
                self.data_source_info = data_source_info_object.output

        else:
            err_msg = ('We currently do not process this file type.'
                       ' Please use a file with one of the following'
                       ' extensions: %s') % \
                      (ACCEPTABLE_EXT_LIST,)
            runner = None
            self.add_error(err_msg)
            return runner, self.error_message


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
            self.add_error(err_msg)
            return None, self.error_message
         except PermissionError as err_obj:
            err_msg = ('No read prermission on this file:'
                       ' \n - File: %s\n - %s') % \
                      (self.input_file, err_obj)
            self.add_error(err_msg)
            return None, self.error_message
         except Exception as err_obj:
            err_msg = ('Failed to load csv file.'
                       ' \n - File: %s\n - %s') % \
                      (self.input_file, err_obj)
            self.add_error(err_msg)
            return None, self.error_message
         # print("*******df********", df)
         self.dataframe = df
         print("datasource", self.data_source_info)


        if format == CSV_FILE_EXT:
            try:
                df = pd.read_csv(self.input_file,
                             delimiter=None)
            except pd.errors.ParserError as err_obj:
                err_msg = ('Failed to load csv file (pandas ParserError).'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                self.add_error(err_msg)
                return None, self.error_message
            except PermissionError as err_obj:
                err_msg = ('No read prermission on this file:'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                self.add_error(err_msg)
                return None, self.error_message
            except Exception as err_obj:
                err_msg = ('Failed to load csv file.'
                           ' \n - File: %s\n - %s') % \
                          (self.input_file, err_obj)
                self.add_error(err_msg)
                return None, self.error_message
            # print("*******df********",df)
            self.dataframe = df
            print("datasource", self.data_source_info)







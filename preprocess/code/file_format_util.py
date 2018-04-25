from __future__ import print_function
from collections import OrderedDict
import decimal
import json, time, datetime
import pandas as pd
import os
from os.path import basename, isdir, isfile, splitext

from preprocess_runner import *
from data_source_info import DataSourceInfo, SOURCE_TYPE_FILE
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
    def __init__(self, input_file, **kwargs):
        """Identify file type: csv, tab, etc"""
        # print("The file format class is called")
        self.input_file = input_file
        self.job_id = kwargs.get('job_id')

        # data source info
        self.file_basename = None
        self.source_type = None
        self.source_format = None

        self.dataframe = None
        self.data_source_info = None

        self.fname_ext = None
        self.fname_ext_check = None





        #
        self.has_error = False
        self.error_message = None

        self.split_filename()
        self.check_file()

    def add_error(self, err):
        self.has_error = True
        self.error_message = err


    def split_filename(self):
        """split the filename"""
        if not self.input_file:
            self.add_error('The "input_file" was %s' % self.input_file)
            return

        # file basename with extension
        #
        self.file_basename = basename(self.input_file)

        # file extenion
        #
        _fname_base, self.fname_ext = splitext(self.file_basename)

        if self.fname_ext:
            self.fname_ext_check = self.fname_ext.lower()


    def check_file(self):
        """ handles all the files"""
        if self.has_error:
            return

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
            self.get_dataframe(TAB_FILE_EXT)
            self.source_type = SOURCE_TYPE_FILE
            self.source_format = TAB_FILE_EXT

            data_source_info_object = DataSourceInfo(name=self.file_basename,
                                                     source_type=self.source_type,
                                                     source_format=self.source_format)

            self.data_source_info = data_source_info_object.data

        elif self.fname_ext_check == CSV_FILE_EXT:
            self.get_dataframe(CSV_FILE_EXT)
            self.source_type = SOURCE_TYPE_FILE
            self.source_format = CSV_FILE_EXT
            data_source_info_object = DataSourceInfo(name=self.file_basename,
                                                     source_type=self.source_type,
                                                     source_format=self.source_format)
            self.data_source_info = data_source_info_object.data

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

    def get_dataframe(self, format_name):
        """ get dataframe on basis of the format"""
        if format_name == TAB_FILE_EXT:
            try:
                data_frame = pd.read_csv(self.input_file,
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
            self.dataframe = data_frame
            print("datasource", self.data_source_info)

        if format_name == CSV_FILE_EXT:
            try:
                data_frame = pd.read_csv(self.input_file,
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
            self.dataframe = data_frame
            print("datasource", self.data_source_info)

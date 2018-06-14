import json
import jsonschema
from jsonschema import validate as jvalidate
from jsonschema import Draft4Validator
from collections import OrderedDict
from os.path import isdir, isfile, join
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)

SUCCESS_MESSAGE = 'Valdiation successfull'
class ValidationUtil(object):

    @staticmethod
    def run_it(schema_file, data_file):


        #print(json.dumps(the_schema, indent=4))
        try:
            Draft4Validator(schema_file)
        except jsonschema.exceptions.ValidationError as err_obj:
            print('Schema Error. short message: ', err_obj.message)
            print('Schema Error. full message: ', err_obj)
            return err_resp(err_obj.message)

        # the_data = get_file_as_dict(data_file)
        #print(json.dumps(the_data, indent=4))
        try:
            Draft4Validator(schema_file).validate(data_file)
        except jsonschema.exceptions.ValidationError as err_obj:
            print('Data Error. short message: ', err_obj.message)
            print('Data Error. full message: ', err_obj)
            return err_resp(err_obj.message)

        return ok_resp(SUCCESS_MESSAGE)
        print('looking good!')

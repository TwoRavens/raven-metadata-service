import json
import jsonschema
from jsonschema import validate as jvalidate
from jsonschema import Draft4Validator
from collections import OrderedDict
from os.path import isdir, isfile, join


def get_file_as_dict(fname):
    """Open the file and load as a dict"""
    fpath = join('input', fname)
    assert isfile(fpath), print('file not found: %s' % fpath)

    print('load file: %s' % fpath)

    info_dict = json.loads(open(fpath, 'r').read())#                          object_pairs_hook=OrderedDict)

    return info_dict


def run_it(schema_fname, data_fname):

    the_schema = get_file_as_dict(schema_fname)
    #print(json.dumps(the_schema, indent=4))
    try:
        Draft4Validator(the_schema)
    except jsonschema.exceptions.ValidationError as err_obj:
        print('Schema Error. short message: ', err_obj.message)
        print('Schema Error. full message: ', err_obj)
        return

    the_data = get_file_as_dict(data_fname)
    #print(json.dumps(the_data, indent=4))
    try:
        Draft4Validator(the_schema).validate(the_data)
    except jsonschema.exceptions.ValidationError as err_obj:
        print('Data Error. short message: ', err_obj.message)
        print('Data Error. full message: ', err_obj)
        return

    print('looking good!')


if __name__ == '__main__':
    #run_it('dataset_schema.json', 'dataset_data_02.json')
    #run_it('variable_schema.json', 'variable_data_01.json')
    run_it('variable_schema_04.json', 'variable_data_03.json')

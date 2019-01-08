import json
from collections import OrderedDict
from np_json_encoder import NumpyJSONEncoder
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)

def json_dump(data_dict, indent=None):
    """Dump JSON to a string w/o indents"""
    if indent is not None and \
        not isinstance(indent, int):
        # quick sanity check
        return err_resp('indent must be None or an integer')

    try:
        # dump it to a string
        jstring = json.dumps(data_dict,
                             indent=indent,
                             cls=NumpyJSONEncoder)
        return ok_resp(jstring)

    except TypeError as err_obj:
        # uh oh
        user_msg = ('Failed to convert to JSON: %s'
                    ' (json_util)\n\n%s') % \
                    (err_obj, str(data_dict)[:200])
        return err_resp(user_msg)



def json_loads(json_str):
    """wrapper for json.loads that outputs an OrderedDict"""
    try:
        json_dict = json.loads(json_str,
                               object_pairs_hook=OrderedDict)
    except json.decoder.JSONDecodeError as err_obj:
        err_msg = 'Failed to convert string to JSON: %s' % (err_obj)
        return err_resp(err_msg)
    except TypeError as err_obj:
        err_msg = 'Failed to convert string to JSON: %s' % (err_obj)
        return err_resp(err_msg)

    return ok_resp(json_dict)


def remove_nan_from_dict(info_dict):
    """For dict (or OrderedDict) objects, that contain np.Nan,
    change np.Nan to None
    reference: https://stackoverflow.com/questions/35297868/how-could-i-fix-the-unquoted-nan-value-in-json-using-python
    """
    if not isinstance(info_dict, dict):
        user_msg = ('"info_dict" must be a dict object'
                    ' (which includes OrderedDict)')
        return err_resp(user_msg)

    # 1 - Dump the info_dict to a string
    #
    json_info = json_dump(info_dict)
    if not json_info.success:
        return err_resp(json_info.err_msg)


    # 2- Within the string, replace 'NaN' with 'null'
    #
    json_str = json_info.result_obj.replace('NaN', 'null')


    # 3 - Load the string back to a dict and return it
    #
    formatted_json_data = json.loads(json_str,
                                     object_pairs_hook=OrderedDict)

    return ok_resp(formatted_json_data)

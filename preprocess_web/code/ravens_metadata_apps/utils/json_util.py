import json
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

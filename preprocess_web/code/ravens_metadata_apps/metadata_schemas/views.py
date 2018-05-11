import json
from collections import OrderedDict
from django.shortcuts import render
from django.http import \
    (JsonResponse, HttpResponse,
     Http404, HttpResponseRedirect,
     QueryDict)
from django.template.loader import render_to_string
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)
import col_info_constants as col_const
from ravens_metadata_apps.utils.json_util import json_dump

#from np_json_encoder import NumpyJSONEncoder

# Create your views here.

temp_schema_pre_models = 'metadata_schemas/variable_schema_12.json'

def view_latest_metadata_schema(request):
    """Return the latest JSON schema for the metadata file"""
    json_string = render_to_string(\
                        temp_schema_pre_models,
                        {})

    # A quick sanity check
    try:
        info_dict = json.loads(json_string)
    except TypeError as err_obj:
        return JsonResponse(get_json_error('Schema is not valid JSON! %s' % err_obj))

    if 'pretty' in request.GET:
        jstring = json_dump(info_dict, indent=4)
        if jstring.success:
            return HttpResponse('<pre>%s</pre>' % jstring.result_obj)
        return JsonResponse(get_json_error(jstring.err_mg))

    return JsonResponse(info_dict)


def view_latest_dataset_schema(request):
    """Return the latest JSON schema for the dataset portion of the metadata file"""

    json_string = render_to_string(\
                        temp_schema_pre_models,
                        {})

    # A quick sanity check
    try:
        info_dict = json.loads(json_string,
                               object_pairs_hook=OrderedDict)
    except TypeError as err_obj:
        return HttpResponse('Schema is not valid JSON! %s' % err_obj,
                            code=400)

    if not 'properties' in info_dict:
        user_msg = 'Schema does not contain a "properties" section' % \
                   col_const.DATASET_LEVEL_KEY
        return HttpResponse(get_json_error(user_msg))

    if not col_const.DATASET_LEVEL_KEY in info_dict['properties']:
        user_msg = 'Schema does not contain a "properties.%s" section' % \
                   col_const.DATASET_LEVEL_KEY
        return HttpResponse(get_json_error(user_msg))

    dataset_dict = info_dict['properties'][col_const.DATASET_LEVEL_KEY]

    if 'pretty' in request.GET:
        jstring = json_dump(dataset_dict, indent=4)
        if jstring.success:
            return HttpResponse('<pre>%s</pre>' % jstring.result_obj)
        return JsonResponse(get_json_error(jstring.err_mg))

    return JsonResponse(dataset_dict)

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
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.metadata_schemas.variable_info import VariableInfo

#from np_json_encoder import NumpyJSONEncoder

# Create your views here.

temp_schema_pre_models = 'metadata_schemas/variable_schema_12.json'


def get_schema_as_dict():
    """Open the schema file and return it as an OrderedDict"""
    json_string = render_to_string(\
                        temp_schema_pre_models,
                        {})

    # A quick sanity check
    try:
        info_dict = json.loads(json_string)
    except TypeError as err_obj:
        return err_resp('Schema is not valid JSON! %s' % err_obj)

    return ok_resp(info_dict)


def view_variable_definitions(request):
    """Helper view to generate .rst file.  This content may be copied into
    docs/source/defn_variables.rst"""
    schema_info = get_schema_as_dict()
    if not schema_info.success:
        return HttpResponse(get_json_error(schema_info.err_msg))


    schema = schema_info.result_obj
    var_info = schema['properties']['variables']\
                     ['patternProperties']['^[_a-zA-Z0-9]+$']\
                     ['properties']

    var_list = []
    for var_name, var_dict in var_info.items():
        print('-' * 40)
        print(var_name)
        print(var_dict)
        var_obj = VariableInfo(var_name, var_dict)
        var_obj.show()
        var_list.append(var_obj)


    info_dict = dict(schema=schema,
                     var_list=var_list)

    return render(request,
                  'metadata_schemas/defn_variables.rst',
                  info_dict)




def view_latest_metadata_schema(request):
    """Return the latest JSON schema for the metadata file"""

    schema_info = get_schema_as_dict()
    if not schema_info.success:
        return JsonResponse(get_json_error(schema_info.err_msg))

    info_dict = schema_info.result_obj

    if 'pretty' in request.GET:
        jstring = json_dump(info_dict, indent=4)

        if jstring.success:
            info = dict(json_schema=jstring.result_obj)
            return render(request,
                          'metadata_schemas/schema_pretty.html',
                          info)
        else:
            return JsonResponse(get_json_error(jstring.err_mg))

    return JsonResponse(info_dict)


def view_latest_dataset_schema(request):
    """Return the latest JSON schema for the dataset portion of the metadata file"""
    schema_info = get_schema_as_dict()
    if not schema_info.success:
        return JsonResponse(get_json_error(schema_info.err_msg))

    info_dict = schema_info.result_obj

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
            info = dict(json_schema=jstring.result_obj)
            return render(request,
                          'metadata_schemas/schema_pretty.html',
                          info)
        return JsonResponse(get_json_error(jstring.err_mg))

    return JsonResponse(dataset_dict)

"""
Utilities for views
"""
from collections import OrderedDict
import json
from urllib.parse import urlparse

from django.http import HttpRequest


KEY_EDITOR_URL = 'EDITOR_URL'
HIDE_VERSIONS_BUTTON = 'HIDE_VERSIONS_BUTTON'
HIDE_EDITOR_BUTTON = 'HIDE_EDITOR_BUTTON'


def get_common_view_info(request):
    """For all pages, e.g. is user logged in, etc"""

    info = dict()

    #info = dict(is_authenticated=request.user.is_authenticated,
    #            user=request.user)

    return info


def get_baseurl_from_request(request):
    """Use the request object to build a base url"""
    assert isinstance(request, HttpRequest),\
        "request must be a django.http.HttpRequest object"""

    urlParts = urlparse(request.build_absolute_uri())

    return '%s://%s' % (urlParts.scheme, urlParts.netloc)

def get_json_error(err_msg, errors=None):
    """return an OrderedDict with success=False + message"""
    info = OrderedDict()
    info['success'] = False
    info['message'] = err_msg
    if errors:
        info['errors'] = errors
    return info

def get_json_success(user_msg, **kwargs):
    """return an OrderedDict with success=True + message + optional 'data'"""
    info = OrderedDict()
    info['success'] = True
    info['message'] = user_msg

    # add on additional data pieces
    for key, val in kwargs.items():
        if key == 'data':
            continue
        info[key] = val

    if 'data' in kwargs:
        info['data'] = kwargs['data']

    return info


def get_session_key(request):
    """Common method to get the session key"""
    assert request, 'request cannot be None'

    return request.session._get_or_create_session_key()


def get_authenticated_user(request):
    """Return the user from the request"""
    if not request:
        return False, 'request is None'

    if not request.user.is_authenticated():
        return False, 'user is not authenticated'

    return True, request.user


def get_request_body(request):
    """Retrieve the request body
    Returns either:
        (True, content text)
        (Fales, error message)
    """
    if not request:
        return False, 'request is None'

    if not request.body:
        return False, 'request.body not found'

    return True, request.body.decode('utf-8')


def get_request_body_as_json(request):
    """Retrieve the request body converted to JSON (python OrderedDict)
    Returns either:
        (True, content text)
        (Fales, error message)
    """
    if not request:
        return False, 'request is None'

    success, req_body_or_err = get_request_body(request)
    if not success:
        return False, req_body_or_err

    try:
        json_data = json.loads(req_body_or_err,
                               object_pairs_hook=OrderedDict)
    except json.decoder.JSONDecodeError as err_obj:
        err_msg = ('Failed to convert request body to JSON: %s') % err_obj
        return False, err_msg
    except TypeError as err_obj:
        err_msg = ('Failed to convert request body to JSON: %s') % err_obj
        return False, err_msg

    return True, json_data

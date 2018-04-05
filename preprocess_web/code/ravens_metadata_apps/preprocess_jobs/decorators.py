"""
View decorator to check for an api_key in the header

"""

from ravens_metadata_apps.raven_auth.models import User, KEY_API_USER
from django.http import JsonResponse, QueryDict


API_ERR_MSG_KEY = 'API_ERR_MSG_KEY'

def bad_api_view(request, *args, **kwargs):

    err_msg = kwargs.get(API_ERR_MSG_KEY, None)
    if err_msg is None:
        err_msg = "Sorry, there was an error with your API key."

    d = dict(status='ERROR',\
            message=err_msg)
    return JsonResponse(d, status=401)


def apikey_required(view_func):
    """View wrapper.  API key required"""

    def check_apikey(request, *args, **kwargs):

        # ---------------------------
        # Assume production, check the API key
        # ---------------------------
        auth_info = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth_info:
            error_message = (\
                "An API key is required."
                '(API key is "api-key" in the header)'
                " Please see [documentation link]")
            kwargs[API_ERR_MSG_KEY] = error_message
            return bad_api_view(request, *args, **kwargs)

        label, api_key = auth_info.split()
        print('type(api_key)', type(api_key))
        print('api_key', api_key)
        #meta_keys.sort()
        #for k in meta_keys:
        #    print('[%s] -> %s' % (k, request.META[k]))
        if api_key is None:
            error_message = (\
                "An API key is required."
                '(API key is "api-key" in the header)'
                " Please see [documentation link]")
            kwargs[API_ERR_MSG_KEY] = error_message
            return bad_api_view(request, *args, **kwargs)

        try:
            user = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            error_message = (\
                "No user was found for that API key."
                " Please see [documentation link]")
            kwargs[API_ERR_MSG_KEY] = error_message
            return bad_api_view(request, *args, **kwargs)

        # ---------------------------
        # OK, Continue on!
        # ---------------------------
        kwargs[KEY_API_USER] = user
        response = view_func(request, *args, **kwargs)

        # (maybe do something after the view_func call)
        #
        return response

    return check_apikey

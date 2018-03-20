from ravens_metadata_apps.preprocess_jobs.models import User

#from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, QueryDict

"""
def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        entry = Entry.objects.get(pk=kwargs['entry_id'])
        if entry.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
"""
API_ERR_MSG_KEY = 'API_ERR_MSG_KEY'

def bad_api_view(request, *args, **kwargs):

    err_msg = kwargs.get(API_ERR_MSG_KEY, None)
    if err_msg is None:
        err_msg = "Sorry, there was an error with your API key."

    d = dict(status='ERROR',\
            message=err_msg)
    return JsonResponse(d)


def apikey_required(view_func):
    """View wrapper.  Dataverse API key required if DEBUG=False"""

    def check_apikey(request, *args, **kwargs):

        # maybe do something before the view_func call
        # that uses `extra_value` and the `request` object
        #if settings.DEBUG is False:

        # ---------------------------
        # Assume production, check the API key
        # ---------------------------
        api_key = request.META.get('api-key', None)
        if api_key is None:
            error_message = (\
                "An API key is required."
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
        kwargs['api_user'] = user
        response = view_func(request, *args, **kwargs)

        # (maybe do something after the view_func call)
        #
        return response

    return check_apikey


'''
def is_api_authorized_user(function):
    """Check the header for either an acceptable token or  username/password"""
    def wrap(request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        api_key = request.META.get('api-token', None)
        try:
            user = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            raise PermissionDenied
        kwargs['api_user'] = user
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
'''

"""Simple url formatting calls wrapping urlparse"""
from urllib.parse import urlparse, parse_qs
from ravens_metadata_apps.utils.basic_response import (err_resp, ok_resp)
from ravens_metadata_apps.dataverse_connect.dv_constants import \
    (KEY_DATAVERSE_FILE_ID)


class URLHelper(object):
    """Helper methods related to urls"""

    @staticmethod
    def get_parsed_url(url_str):
        """Return a ParseResult object"""
        if not url_str:
            return err_resp('A url is required')

        if not isinstance(url_str, str):
            return err_resp('The "url_str" must be a string')

        return ok_resp(urlparse(url_str))

    @staticmethod
    def get_netloc_from_url(url_str):
        """Return the netloc from the url"""
        info = URLHelper.get_parsed_url(url_str)
        if not info.success:
            return info

        netloc = info.result_obj
        if not netloc:
            return err_resp('The "url_str" did not contain a server name.')

        return ok_resp(netloc.lower())


    @staticmethod
    def format_url_for_saving(url_str, remove_trailing_slash=True):
        """Make the url lowercase, etc."""
        netloc_info = URLHelper.get_netloc_from_url(url_str)
        if not netloc_info.success:
            return netloc_info

        if remove_trailing_slash:
            while url_str and url_str.endswith('/'):
                url_str = url_str[:-1]

        return ok_resp(url_str.lower())

    @staticmethod
    def get_datafile_id_from_url(url_str):
        """Return the datafile from the query params
        Ex/: https://dataverse.harvard.edu/file.xhtml?fileId=3135445&version=RELEASED&version=.0"""
        info = URLHelper.get_parsed_url(url_str)
        if not info.success:
            return info

        params = parse_qs(info.result_obj.query)
        if KEY_DATAVERSE_FILE_ID in params and params[KEY_DATAVERSE_FILE_ID]:
            return ok_resp(params[KEY_DATAVERSE_FILE_ID])

        return err_resp('No %s in the url query string: %s' % \
                        info.result_obj.query)

"""Simple url formatting calls wrapping urlparse"""
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from ravens_metadata_apps.utils.basic_response import err_resp, ok_resp
from ravens_metadata_apps.dataverse_connect.dv_constants import \
    (KEY_DATAVERSE_FILE_ID, KEY_DATAVERSE_FILE_VERSION,
     PATH_DATAFILE_ACCESS)


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

        netloc = info.result_obj.netloc
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
        """Return the datafile id from the path or query params
            - https://dataverse.harvard.edu/api/access/datafile/3135445
            - https://dataverse.harvard.edu/file.xhtml?fileId=3135445&version=RELEASED&version=.0"""
        info = URLHelper.get_parsed_url(url_str)
        if not info.success:
            return info

        # Is the file id in the path?
        #
        url_path = info.result_obj.path.lower()
        if url_path.startswith(PATH_DATAFILE_ACCESS):
            dv_id = url_path.replace(PATH_DATAFILE_ACCESS, '')
            if not str(dv_id).isdigit():
                return err_resp('The file id is not an integer: "%s"' % dv_id)

            return ok_resp(int(dv_id))


        # Check for the fileId the query string
        #
        params = parse_qs(info.result_obj.query)

        if not params:
            return err_resp('The file id was not found in the url or query'
                            ' string: "%s"' % (url_str))

        # retrieve the required keys
        #
        if KEY_DATAVERSE_FILE_ID in params and params[KEY_DATAVERSE_FILE_ID]:
            dv_id = params[KEY_DATAVERSE_FILE_ID]
            if isinstance(dv_id, list) and dv_id:
                dv_id = dv_id[0]

            if not str(dv_id).isdigit():
                return err_resp('The file id is not an integer: "%s"' % dv_id)

            return ok_resp(int(dv_id))

        return err_resp('No "%s" key in the url query string: %s' % \
                        (KEY_DATAVERSE_FILE_ID, info.result_obj.query))


    @staticmethod
    def format_datafile_request_url(url_str):
        """Return a formatted datafile request with a consistent case, etc."""
        info = URLHelper.get_parsed_url(url_str)
        if not info.success:
            return info

        parsed = info.result_obj

        datafile_info = URLHelper.get_datafile_id_from_url(url_str)
        if not datafile_info.success:
            return err_resp(datafile_info.err_msg)

        params = urlencode({KEY_DATAVERSE_FILE_ID: datafile_info.result_obj})

        fmt_url = urlunparse((parsed.scheme,
                              parsed.netloc.lower(),
                              parsed.path.lower(),
                              params))

        return ok_resp(fmt_url)


    @staticmethod
    def set_netloc_and_scheme(url_str, reg_dv_obj):
        """Update the RegisteredDataverse or other object"""
        if not reg_dv_obj:
            return err_resp('There is not RegisteredDataverse object, e.g. reg_dv_obj')

        # Update the Dataverse url
        #
        url_info = URLHelper.format_url_for_saving(url_str)
        if not url_info.success:
            return err_resp(\
            "There is something wrong with the url: %s" % url_info.err_msg)

        reg_dv_obj.dataverse_url = url_info.result_obj

        # Add the netloc
        #
        netloc_info = URLHelper.get_netloc_from_url(url_str)
        if not netloc_info.success:
            return err_resp(\
                ("There is something wrong with the url: %s") \
                 % netloc_info.err_msg)
        reg_dv_obj.network_location = netloc_info.result_obj

        # Add the scheme
        #
        parsed_url = URLHelper.get_parsed_url(url_str)
        if not parsed_url.success:
            return err_resp(parsed_url.err_msg)

        reg_dv_obj.url_scheme = parsed_url.result_obj.scheme

        return ok_resp('it worked')

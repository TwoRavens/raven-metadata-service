"""Interim workaround for pulling citation information based on a file id"""
import requests
from ravens_metadata_apps.utils.basic_err_check import BasicErrCheck


class CitationRetriever(BasicErrCheck):
    """Used for pulling Dataverse Citations based on file id"""
    def __init__(self, datafile_id, registered_dataverse):

        self.datafile_id = datafile_id
        self.registered_dataverse = registered_dataverse
        self.dataset_doi = None
        self.citation_as_jsonld = None

        self.retrieve_citation()

    def get_citation(self):
        """return the citation"""
        assert not self.has_error(), \
            "Please check that 'has_error()' is False before using this method"
        return self.citation_as_jsonld


    def get_dataset_doi(self):
        """return the doi"""
        assert not self.has_error(), \
            "Please check that 'has_error()' is False before using this method"
        return self.dataset_doi

    def retrieve_citation(self):
        """go through the steps needed for the citation"""
        if not self.datafile_id:
            self.add_err_msg('datafile_id must be set')
            return

        self.call_search_api_for_doi()
        if self.dataset_doi:
            self.call_jsonld_api()


    def call_jsonld_api(self):
        """Retrieve the JSON-LD citation"""
        if self.has_error():
            return

        jsonld_url = self.registered_dataverse.get_jsonld_url(self.dataset_doi)

        # Call Dataverse....
        #
        try:
            result2 = requests.get(jsonld_url)
        except requests.exceptions.ConnectionError as err_obj:
            user_msg = ('Failed to retrieve JSON-LD from %s'
                        '\nError: %s') % (jsonld_url, err_obj)
            self.add_err_msg(user_msg)
            return

        # Check the response codes
        #
        if result2.status_code != requests.codes.ok:
            user_msg = ('Failed to retrieve doi from %s') % \
                        (jsonld_url)

            if result2.status_code == requests.codes.not_found:
                user_msg = ('%s\nThe file was not found.') % user_msg
            elif result2.status_code == requests.codes.forbidden:
                user_msg = ('%s\nThe url is forbidden--likely an unpublished'
                            ' file.') % \
                            user_msg

            user_msg = ('%s\nStatus code: %s') % (user_msg, result2.status_code)

            self.add_err_msg(user_msg)
            return

        # Convert the result to JSON
        #
        try:
            self.citation_as_jsonld = result2.json()
        except Exception as err_obj:
            user_msg = ('Failed to convert JSON-LD to JSON from: %s'
                        '\n%s') % \
                        (self.search_url, err_obj)
            self.add_err_msg(user_msg)
            return



    def call_search_api_for_doi(self):
        """Use the Dataverse search API to retrieve the file's DOI"""
        if self.has_error():
            return

        search_url = self.registered_dataverse.get_search_api_url(self.datafile_id)

        # Call Dataverse....
        #
        try:
            result1 = requests.get(search_url)
        except requests.exceptions.ConnectionError as err_obj:
            user_msg = ('Failed to retrieve doi from %s'
                        '\nError: %s') % (search_url, err_obj)
            self.add_err_msg(user_msg)
            return

        # Check the response codes
        #
        if result1.status_code != requests.codes.ok:
            user_msg = ('Failed to retrieve doi from %s') % \
                        (self.search_url)

            if result1.status_code == requests.codes.not_found:
                user_msg = ('%s\nThe file was not found.') % user_msg
            elif result1.status_code == requests.codes.forbidden:
                user_msg = ('%s\nThe url is forbidden--likely an unpublished'
                            ' file.') % \
                            user_msg

            user_msg = ('%s\nStatus code: %s') % (user_msg, result1.status_code)

            self.add_err_msg(user_msg)
            return


        # Convert the result to JSON
        #
        try:
            json_result = result1.json()
        except Exception as err_obj:
            user_msg = ('Failed to convert search results to JSON from: %s'
                        '\n%s') % \
                        (self.search_url, err_obj)
            self.add_err_msg(user_msg)
            return

        self.pull_doi_from_json_citation(json_result, search_url)


    def pull_doi_from_json_citation(self, json_result, search_url):
        """Parse the search results in an attempt to pull out the DOI"""
        if self.has_error():
            return

        if not isinstance(json_result, dict):
            self.add_err_msg('Invalid value.  The json_result must be a dict.')
            return

        try:
            result_cnt = json_result['data']['total_count']
        except KeyError as err_obj:
            user_msg = ('This may not be a Datafile url.'
                        '\nKey not found in json_result: %s'
                        '\nSearch url: %s\n%s') % \
                        (json_result, search_url, err_obj)
            self.add_err_msg(user_msg)
            return

        if result_cnt != 1:
            user_msg = ('Expected a single result from the search.'
                        ' Found: %s'
                        '\nSearch url: %s\n%s') % \
                        (result_cnt, search_url, json_result)
            self.add_err_msg(user_msg)
            return

        try:
            dataset_citation = json_result['data']['items'][0]['dataset_citation']
        except IndexError as err_obj:
            user_msg = ('Index error when retrieving "dataset_citation" from'
                        ' data.items[0]: %s'
                        '\nSearch url: %s\n%s') % \
                        (json_result, search_url, err_obj)
            self.add_err_msg(user_msg)
            return
        except KeyError as err_obj:
            user_msg = ('This may not be a Datafile url.'
                        '\nKey not found in json_result: %s\n%s') % \
                        (json_result, err_obj)
            self.add_err_msg(user_msg)
            return

        start_idx = dataset_citation.find('doi.org')
        if start_idx == -1:
            user_msg = ('"doi.org" not found in dataset_citation: %s'
                        '\nsearch_url: %s') % \
                        (dataset_citation, search_url)
            self.add_err_msg(user_msg)
            return

        end_idx = dataset_citation.find(',', start_idx)
        if end_idx == -1:
            user_msg = ('"doi.org" ending not found in dataset_citation: %s'
                        '\nsearch_url: %s') % \
                        (dataset_citation, search_url)
            self.add_err_msg(user_msg)
            return

        self.dataset_doi = dataset_citation[start_idx:end_idx]

        print('self.dataset_doi', self.dataset_doi)
        #data.items[0].dataset_citation' | grep -o 'https://doi.*' | cut -d, -f1`

"""
import re

citation = '''Tchernichovski, Ofer, 2018, \"Ratings of simulated ferry services and matches estimation\", https://doi.org/10.7910/DVN/OCYAPW, Harvard Dataverse, V1"'''

match = re.search(r'(doi/[\w\.-/]+),', citation)
print(match.group()) # The whole matched text
print(match.group(1)) # The username (group 1)
print(match.group(2)) # The host (group 2)
"""

"""
DOI=`echo $DOI_URL | sed 's/https:\/\/doi/doi:/' | sed 's/\.org\///
    {"status":"OK","data":{"q":"entityId:3148839","total_count":1,"start":0,"spelling_alternatives":{},"items":[{"name":"FerryDataDepositFinal.mat","type":"file","url":"https://dataverse.harvard.edu/api/access/datafile/3148839","file_id":"3148839","description":"Ratings data mat file. Each experiment is stored in three variables: subjects=subject ID, delay=ferry service delay (in seconds), score (rating score from 1-100). ","published_at":"2018-05-02T19:28:28Z","file_type":"Unknown","file_content_type":"application/octet-stream","size_in_bytes":214986,"md5":"4c9309f654b92da403fe84b54956c477","checksum":{"type":"MD5","value":"4c9309f654b92da403fe84b54956c477"},"dataset_citation":"Tchernichovski, Ofer, 2018, \"Ratings of simulated ferry services and matches estimation\", https://doi.org/10.7910/DVN/OCYAPW, Harvard Dataverse, V1"}],"count_in_response":1}}
"""

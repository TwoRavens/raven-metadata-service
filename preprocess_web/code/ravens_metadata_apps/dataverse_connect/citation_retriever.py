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

    def retrieve_citation(self):
        """go through the steps needed for the citation"""
        if not self.datafile_id:
            self.add_err_msg('datafile_id must be set')
            return

        search_url = self.registered_dataverse.get_search_api_url(self.datafile_id)

        try:
            result1 = requests.get(search_url)
        except requests.exceptions.ConnectionError as err_obj:
            user_msg = ('Failed to retrieve doi from %s'
                        '\nError: %s') % (search_url, err_obj)
            self.add_err_msg(user_msg)
            return

        if result1.status_code != requests.codes.ok:
            user_msg = ('Failed to retrieve doi from %s') % \
                        (self.search_url)

            if result1.status_code == requests.codes.not_found:
                user_msg = ('%s\nThe file was not found.') % user_msg
            elif result1.status_code == requests.codes.forbidden:
                user_msg = ('%s\nThe url is forbidden--likely an unpublished'
                            ' file.') % \
                            user_msg

            user_msg = ('%s\nStatus code: %s') % (user_msg, request.status_code)

            self.add_err_msg(user_msg)
            return


        try:
            json_result = result1.json()
        except Exception as err_obj:
            user_msg = ('Failed to convert result to JSON from: %s'
                        '\n%s') % \
                        (self.search_url, err_obj)
            self.add_err_msg(user_msg)
            return

        try:
            result_cnt = json_result['data']['total_count']
        except KeyError as err_obj:
            user_msg = ('Key not found in json_result: %s\n%s') % \
                        (json_result, err_obj)
            self.add_err_msg(user_msg)
            return

        if result_cnt != 1:
            user_msg = ('Key not found in json_result: %s\n%s') % \
                        (json_result, err_obj)
            self.add_err_msg(user_msg)
            return

        try:
            dataset_citation = json_result['data']['items'][0]['dataset_citation']
        except KeyError as err_obj:
            user_msg = ('Key not found in json_result: %s\n%s') % \
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
DOI=`echo $DOI_URL | sed 's/https:\/\/doi/doi:/' | sed 's/\.org\///
    {"status":"OK","data":{"q":"entityId:3148839","total_count":1,"start":0,"spelling_alternatives":{},"items":[{"name":"FerryDataDepositFinal.mat","type":"file","url":"https://dataverse.harvard.edu/api/access/datafile/3148839","file_id":"3148839","description":"Ratings data mat file. Each experiment is stored in three variables: subjects=subject ID, delay=ferry service delay (in seconds), score (rating score from 1-100). ","published_at":"2018-05-02T19:28:28Z","file_type":"Unknown","file_content_type":"application/octet-stream","size_in_bytes":214986,"md5":"4c9309f654b92da403fe84b54956c477","checksum":{"type":"MD5","value":"4c9309f654b92da403fe84b54956c477"},"dataset_citation":"Tchernichovski, Ofer, 2018, \"Ratings of simulated ferry services and matches estimation\", https://doi.org/10.7910/DVN/OCYAPW, Harvard Dataverse, V1"}],"count_in_response":1}}
"""

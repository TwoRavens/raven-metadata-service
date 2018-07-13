"""Used when working with Dataverse"""

# https://dataverse.harvard.edu/file.xhtml?fileId=3135445&version=RELEASED&version=.0
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MZIBKB
# http://dataverse.harvard.edu/api/access/datafile/:persistentId/?persistentId=doi:10.5072/FK2/J8SJZB
#
KEY_DATAVERSE_FILE_ID = 'fileId'
KEY_DATAVERSE_FILE_VERSION = 'version'

PATH_DATAFILE_ACCESS = '/api/access/datafile/'
PATH_DATAFILE_ACCESS_PERSISTENT_ID = '/api/access/datafile/:persistentId/?persistentId='
PATH_DATAFILE_PAGE = '/file.xhtml'

KEY_DATAVERSE_PERSISTENT_ID = 'persistentId'
PATH_DATASET_PAGE = 'dataset.xhtml'  # for dataset, can be used

'''Contants used in the preprocess logic and metadata output'''
PREPROCESS_ID = 'preprocessId'

SELF_SECTION_KEY = 'self'
VERSION_KEY = 'version'
VARIABLES_SECTION_KEY = 'variables'
VARIABLE_DISPLAY_SECTION_KEY = 'variableDisplay'

# -----------------------------
# dataset
# -----------------------------
DATASET_LEVEL_KEY = 'dataset'

DATASET_ROW_CNT = 'rowCount'
DATASET_VARIABLE_CNT = 'variableCount'
DATASET_CITATION = 'citation'

DATA_SOURCE_INFO = 'dataSource'
DATA_SOURCE_NAME = 'name'
DATA_SOURCE_TYPE = 'type'
DATA_SOURCE_FORMAT = 'format'
DATA_SOURCE_FILESIZE = 'filesize'


NOT_IMPLEMENTED = 'NOT IMPLEMENTED'
NOT_APPLICABLE = 'NA'
# --------------------------------------
# numchar constants for metadata file
# --------------------------------------
NUMCHAR_LABEL = 'numchar'

NUMCHAR_NUMERIC = 'numeric'
NUMCHAR_CHARACTER = 'character'

NUMCHAR_VALUES = (NUMCHAR_NUMERIC,
                  NUMCHAR_CHARACTER)

# --------------------------------------
# interval constants for metadata file
# --------------------------------------
INTERVAL_CONTINUOUS = 'continuous'
INTERVAL_DISCRETE = 'discrete'
INTERVAL_VALUES = (INTERVAL_CONTINUOUS,
                   INTERVAL_DISCRETE)

# --------------------------------------
# nature constants for metadata file
# --------------------------------------
NATURE_LABEL = 'nature'

NATURE_NOMINAL = 'nominal'
NATURE_ORDINAL = 'ordinal'
NATURE_INTERVAL = 'interval'
NATURE_RATIO = 'ratio'
NATURE_PERCENT = 'percent'
NATURE_OTHER = 'other'
NATURE_VALUES = (NATURE_NOMINAL,
                 NATURE_ORDINAL,
                 NATURE_INTERVAL,
                 NATURE_RATIO,
                 NATURE_PERCENT,
                 NATURE_OTHER)

# --------------------------------------
# binary constants for metadata file
# --------------------------------------
BINARY_YES = 'yes'
BINARY_NO = 'no'
BINARY_VALUES = (BINARY_YES,
                 BINARY_NO)

# --------------------------------------
# time constants for metadata file
# --------------------------------------
TIME_UNKNOWN = 'unknown'
TIME_YES = 'yes'
TIME_NO = 'no'
TIME_VALUES = (TIME_YES,
               TIME_NO)

# --------------------------------------
# plot types for metadata file
# --------------------------------------
PLOT_BAR = "bar"
PLOT_CONTINUOUS = "continuous"

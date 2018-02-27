'''Contants used in the preprocess logic and metadata output'''

NOT_IMPLEMENTED = 'NOT IMPLEMENTED'
NOT_APPLICABLE = 'NA'
# --------------------------------------
# numchar constants for metadata file
# --------------------------------------
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
NATURE_NOMINAL = 'nominal'
NATURE_ORDINAL = 'ordinal'
NATURE_INTERVAL = 'interval'
NATURE_RATIO = 'ratio'
NATURE_PERCENT = 'percent'
NATURE_DICHOTOMOUS = 'dichotomous'
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
ORDINAL_COUNT = 'count'
DICHOTOMOUS_LOGICAL = 'logical'
DICHOTOMOUS_BINARY = 'logical'
DICHOTOMOUS_OTHER = 'other'
TIME = 'time'
PERCENT_01 = '0-1'
PERCENT_100 = '0-100'

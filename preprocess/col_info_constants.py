'''Contants used in the preprocess logic and metadata output'''

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
TIME_YES = 'yes'
TIME_NO = 'no'
TIME_VALUES = (TIME_YES,
               TIME_NO)

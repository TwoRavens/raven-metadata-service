import pandas as pd
import numpy as np


def is_logical(series):
    """Check if series is logical (boolean)"""
    if series.dtype == 'bool':
        # Looks good, dtype is bool
        #
        return True

    elif series.dtype != 'object':
        # A dtype of "object" may sometimes be a bool;
        # but this isn't an object
        #
        return False

    # --------------------------------------------
    # Examine the object to see if it valid values:
    #   True, False, NAN
    # --------------------------------------------

    # get unique values
    #
    uniques = series.unique().tolist()

    # Remove the valid values from the uniques list
    #
    for valid_val in [True, False, np.nan]:
        if valid_val in uniques:
            uniques.remove(valid_val)

    # If the list is empty then consider it a logical series
    #
    if len(uniques) == 0:
        return True

    # There are still other values in the list, not a logical series
    #
    return False

if __name__ == '__main__':
    s = pd.Series([True, True, False, np.nan, 'boat'])
    print(is_logical(s))

    s = pd.Series([True, True, False, np.nan, ])
    print(is_logical(s))

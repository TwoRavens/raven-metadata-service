from type_guess_series import *
import pandas as pd
import numpy as np


#series = pd.Series([True, False, True, True, np.nan])  # ['discrete', 'dichotomous', 'logical']
#series = pd.Series([1.3243, 21.123123, 65.3242342, 0.44])  # ['continuous', 'ratio']
#series = pd.Series([0, 1, 1, 0])  # ['discrete', 'ordinal', 'count']
#series = pd.Series(['Male', 'Female', 'Male', 'Female'])  # ['discrete', 'ordinal', 'count']
#series = pd.Series(['India', 'USA', 'Italy', 'France'])  # ['discrete', 'ordinal', 'count']
#series = pd.Series([0.33, 0.45, 0.56, 0.68, 0.90])  # ['continuous', 'percent', '0-1']
#series = pd.Series([34.00, 45.00, 65.00, 11.00, 66.34, 99.33])  # ['continuous', 'percent', '0-100']
#series = pd.Series([34.00, 45.00, 65.00, 21.00, 66.34, 99.33])  # ['continuous', 'ratio']

TypeGuessSeries(series, ' UN')

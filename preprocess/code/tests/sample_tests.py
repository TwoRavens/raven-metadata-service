import pandas as pd
import numpy as np

from scipy import stats
from sklearn.neighbors import KernelDensity
from scipy.stats import gaussian_kde
from statsmodels.nonparametric.kde import KDEUnivariate


cnt_min = None
val_min = None
cnt_max = None
val_max = None
output = []
col_data = pd.Series([261, 29, 33, 15, 39, 28, 95, 5, 6, 28, 69, 8, 105, 38, 15])
col_data1 = pd.Series(["India", "USA", "India", "USA", "France", "Japan"])
# # col_data= pd.Series([2,4,5,6])
# col_data.dropna(inplace=True)
# total_sum = sum(col_data)
# fraction_val = []
# for val, cnt in col_data.items():
#     fraction_val.append(np.math.pow(cnt / total_sum, 2))
#
# print(sum(fraction_val))

# for col_val, val_cnt in col_data.value_counts(sort=True, ascending=True).iteritems():
#     print()
#     if cnt_min is None and val_min is None and cnt_max is None and val_max is None:
#         print("here", col_val,val_cnt)
#
#         cnt_min = val_cnt
#         val_min = col_val
#         cnt_max = val_cnt
#         val_max = col_val
#
#     if val_cnt == cnt_max:
#             # val_cnt = cnt_max
#             output.append(col_val)
#             # print(" append ", col_val , val_cnt)
#     elif val_cnt > cnt_max:
#             cnt_max = val_cnt
#             output.clear()
#             output.append(col_val)
#             # print(" clear and append", col_val, val_cnt)
#
#
# print(output)

# total_sum = 0
#
#
# for col_val, val_cnt in col_data1.value_counts().iteritems():
#     total_sum = total_sum + val_cnt
#
# print(total_sum)


kernel = stats.gaussian_kde(col_data)


print(kernel.__dict__)



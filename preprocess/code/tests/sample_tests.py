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
val = pd.Series([
            -95.4940990854581,
            -83.4739317758476,
            -71.453764466237,
            -59.4335971566265,
            -47.413429847016,
            -35.3932625374054,
            -23.3730952277949,
            -11.3529279181844,
            0.667239391426165,
            12.6874067010367,
            24.7075740106472,
            36.7277413202578,
            48.7479086298683,
            60.7680759394788,
            72.7882432490894,
            84.8084105586999,
            96.8285778683104,
            108.848745177921,
            120.868912487532,
            132.889079797142,
            144.909247106753,
            156.929414416363,
            168.949581725974,
            180.969749035584,
            192.989916345195,
            205.010083654805,
            217.030250964416,
            229.050418274026,
            241.070585583637,
            253.090752893247,
            265.110920202858,
            277.131087512468,
            289.151254822079,
            301.17142213169,
            313.1915894413,
            325.211756750911,
            337.231924060521,
            349.252091370132,
            361.272258679742,
            373.292425989353,
            385.312593298963,
            397.332760608574,
            409.352927918184,
            421.373095227795,
            433.393262537405,
            445.413429847016,
            457.433597156626,
            469.453764466237,
            481.473931775848,
            493.494099085458 ])
x = np.linspace(min(val), max(val), len(val))
kernel = stats.gaussian_kde(val)


print(kernel(np.sort(val)))



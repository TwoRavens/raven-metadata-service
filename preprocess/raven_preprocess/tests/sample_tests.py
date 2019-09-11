import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde

#
# cnt_min = None
# val_min = None
# cnt_max = None
# val_max = None
# output = []
# col_data = pd.Series([261, 29, 33, 15, 39, 28, 95, 5, 6, 28, 69, 8, 105, 38, 15])
# col_data1 = pd.Series(["India", "USA", "India", "USA", "France", "Japan"])
# cylinders = pd.Series([])
#
# for i in range(397):
#     output.append(i)
#
# # # col_data= pd.Series([2,4,5,6])
# # col_data.dropna(inplace=True)
# # total_sum = sum(col_data)
# # fraction_val = []
# # for val, cnt in col_data.items():
# #     fraction_val.append(np.math.pow(cnt / total_sum, 2))
# #
# # print(sum(fraction_val))
#
# # for col_val, val_cnt in col_data.value_counts(sort=True, ascending=True).iteritems():
# #     print()
# #     if cnt_min is None and val_min is None and cnt_max is None and val_max is None:
# #         print("here", col_val,val_cnt)
# #
# #         cnt_min = val_cnt
# #         val_min = col_val
# #         cnt_max = val_cnt
# #         val_max = col_val
# #
# #     if val_cnt == cnt_max:
# #             # val_cnt = cnt_max
# #             output.append(col_val)
# #             # print(" append ", col_val , val_cnt)
# #     elif val_cnt > cnt_max:
# #             cnt_max = val_cnt
# #             output.clear()
# #             output.append(col_val)
# #             # print(" clear and append", col_val, val_cnt)
# #
# #
# # print(output)
#
# # total_sum = 0
# #
# #
# # for col_val, val_cnt in col_data1.value_counts().iteritems():
# #     total_sum = total_sum + val_cnt
# #
# # print(total_sum)
# val = pd.Series([1.0,
#                 9.081632653061224,
#                 17.163265306122447,
#                 25.24489795918367,
#                 33.326530612244895,
#                 41.408163265306115,
#                 49.48979591836734,
#                 57.57142857142857,
#                 65.65306122448979,
#                 73.73469387755101,
#                 81.81632653061223,
#                 89.89795918367346,
#                 97.97959183673468,
#                 106.0612244897959,
#                 114.14285714285714,
#                 122.22448979591836,
#                 130.30612244897958,
#                 138.3877551020408,
#                 146.46938775510202,
#                 154.55102040816325,
#                 162.63265306122446,
#                 170.7142857142857,
#                 178.79591836734693,
#                 186.87755102040813,
#                 194.95918367346937,
#                 203.0408163265306,
#                 211.1224489795918,
#                 219.20408163265304,
#                 227.28571428571428,
#                 235.36734693877548,
#                 243.44897959183672,
#                 251.53061224489792,
#                 259.61224489795916,
#                 267.69387755102036,
#                 275.7755102040816,
#                 283.85714285714283,
#                 291.93877551020404,
#                 300.0204081632653,
#                 308.1020408163265,
#                 316.1836734693877,
#                 324.2653061224489,
#                 332.3469387755102,
#                 340.4285714285714,
#                 348.5102040816326,
#                 356.59183673469386,
#                 364.67346938775506,
#                 372.75510204081627,
#                 380.83673469387753,
#                 388.91836734693874,
#                 397.0])
# kernel = stats.gaussian_kde(output)
# value = kernel(val)
#
# print(kernel.dataset)
# print(value.size)
#
# plt.plot(val, value, 'r', label="KDE estimation", color="blue")
# plt.hist(output, normed=10, color="cyan", alpha=.8)
# plt.legend()
# plt.title("d3mIndex plot")
# plt.show()
#


data = pd.read_csv("/Users/kripanshubhargava/Desktop/raven-metadata-service/preprocess/input/learningData.csv")
df = pd.DataFrame(data)
df.dropna(inplace=True)
input_data = []
# print(list(df.columns[0]))
for val in df:
    print(val)
    input_data = df[val]
    kernel = stats.gaussian_kde(input_data)
    x = np.linspace(min(input_data) - kernel.factor, max(input_data)+ kernel.factor, num=50)

    print(kernel.factor)
    print(" covariance, " , kernel.covariance_factor)
    value = kernel(x)
    plt.plot(x, value, 'r', label="KDE estimation", color="blue")
    plt.hist(input_data, normed=10, color="cyan", alpha=.8)
    plt.legend()
    plt.title(input_data.head())
    plt.show()


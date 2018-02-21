import numpy as np
import pandas as pd

from column_info import ColumnInfo
import col_info_constants as col_const


class CalSumStatsUtil(object):

    """This module does the calculation of statistics variables."""
    def __init__(self, col_series, col_info):
        assert isinstance(col_series, pd.Series), "col_series must be a pandas.Series object"
        assert isinstance(col_info, ColumnInfo), "col_info must be a ColumnInfo object"

        self.col_info = col_info
        self.colname = self.col_info.colname
        self.col_series = col_series

        self.calc_stats()

    def calc_stats(self):
        """This method does the calculation of statistics variables."""
        self.col_series.dropna(inplace=True)
        # --------------------------
        # similar to preprocess.R "Mode" function
        # --------------------------
        self.col_info.uniques = len(self.col_series.unique())

        mid_pt = int(self.col_info.uniques / 2)

        # iterate through value_counts for mode stats
        #
        row_num = 0
        cnt_min = None
        val_min = None
        cnt_max = None
        val_max = None
        output = []
        fewest_output = []
        for col_val, val_cnt in self.col_series.value_counts(sort=True, ascending=True).iteritems():
            if cnt_min is None and val_min is None and cnt_max is None and val_max is None:
                cnt_min = val_cnt
                val_min = col_val
                cnt_max = val_cnt
                val_max = col_val

            row_num += 1
            if row_num == mid_pt:
                self.col_info.mid = col_val
                self.col_info.freqmid = val_cnt

            if val_cnt == cnt_max:
                output.append(col_val)
                self.col_info.freqmode = val_cnt
            elif val_cnt > cnt_max:
                cnt_max = val_cnt
                output.clear()
                output.append(col_val)
                self.col_info.freqmode = val_cnt

            if val_cnt == cnt_min:
                fewest_output.append(col_val)
                self.col_info.freqfewest = val_cnt
            elif val_cnt < cnt_min:
                cnt_min = val_cnt
                fewest_output.clear()
                fewest_output.append(col_val)
                self.col_info.freqfewest = val_cnt

        self.col_info.fewest = fewest_output

        self.col_info.mode = output

        if self.col_info.is_character():

            # self.col_info.herfindahl=self.herfindahl_index(self.col_series)
            self.col_info.median = col_const.NOT_APPLICABLE
            self.col_info.max = col_const.NOT_APPLICABLE
            self.col_info.min = col_const.NOT_APPLICABLE
            self.col_info.mean = col_const.NOT_APPLICABLE
            self.col_info.std_dev = col_const.NOT_APPLICABLE

        elif self.col_info.is_numeric():

            self.col_info.median = self.col_series.median()
            self.col_info.max = self.col_series.max()
            self.col_info.min = self.col_series.min()
            self.col_info.mean = self.col_series.mean()
            self.col_info.std_dev = self.col_series.std()
            self.col_info.herfindahl = self.herfindahl_index(\
                                                self.col_series,
                                                drop_missing=False)

            # self.col_info.mode = np.around(self.col_info.mode, 4)
            self.col_info.fewest = np.around(self.col_info.fewest, 4)
            self.col_info.mid = np.around(self.col_info.mid, 4)
            # freqfewest and freqmid left for now as they always give int value. why SignIf then?
            # print("--"*20)
            # print("name : ", self.col_info.colname)
            # print("mode : ", self.col_info.mode)
            # print("fewest : ", self.col_info.fewest)
            # print("mid : ", self.col_info.mid)

    @staticmethod
    def herfindahl_index(col_data, drop_missing=True):
        # check again with the logic of calculating, what values are squared
        """Calculate Herfindahl-Hirschman Index (HHI) for the column data.
        For each given day, HHI is defined as a sum of squared weights of
        %values in a col_series; and varies from 1/N to 1.
        """
        if drop_missing:
            # redundant if not used as a staticmethod,
            # already happens at calc_stats init
            col_data.dropna(inplace=True)

        total_sum = sum(col_data)
        fraction_val = []
        for val, cnt in col_data.items():
            fraction_val.append(np.math.pow(cnt / total_sum, 2))

        return sum(fraction_val)

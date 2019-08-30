"""
Run all tests from /preprocess/raven_preprocess
> python -m unittest

Running 1 file at a time from /preprocess/raven_preprocess

```
# Test type guess
python -m unittest tests.test_type_guess.TestTypeGuess

# Test summary stats
python -m unittest tests.test_summary_stats.SummaryStatsUtilTest

# Test plot values
python -m unittest tests.test_plot_values.PlotValuesTest

# Test update preprocess
python -m unittest tests.test_update_preprocess.UpdatePreprocessTest

# Test preprocess
python -m unittest tests.test_preprocess.PreprocessTest

```
"""
import os, sys
from os.path import abspath, dirname
#sys.path.append(dirname(dirname(abspath(__file__))))

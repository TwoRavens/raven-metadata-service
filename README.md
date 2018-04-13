[![Build Status](https://travis-ci.org/TwoRavens/raven-metadata-service.svg?branch=master)](https://travis-ci.org/TwoRavens/raven-metadata-service.svg)

(note! under initial development. very pre-alpha, etc)

---

# raven-metadata-service

Service to produce TwoRavens metadata.  Description of the produced metadata: http://two-ravens-metadata-service.readthedocs.io

## Install

Prerequisites:
  - python3
  - [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)


Open a Terminal, from the top of this repository, run:

```
# from within ~/raven-metadata-service
mkvirtualenv preprocess
pip install -r requirements/30_preprocess_web.txt
```

## Preprocess a single file from the command line

Open a Terminal, from the top of this repository, run:

```
# from within ~/raven-metadata-service
workon preprocess
cd preprocess_web/code

# -------------------------
# Preprocess a single file,
# Write output to screen
# -------------------------
fab run_preprocess:[input file name]

# Example:
fab run_preprocess:../../test_data/fearonLaitin.csv


# -------------------------
# Preprocess a single file,
# Write output to file
# -------------------------
fab run_preprocess:[input file name],[output file]
fab run_preprocess:../../test_data/fearonLaitin.csv,/tmp/fearonLaitin.json
```

## General preprocess workflow

This gives an overview of the code within `raven-metadata-service/preprocess/code`

### PreprocessRunner
  - Object that handles overall preprocess logic
  - file: `preprocess_runner.py`

**How it is used:**

1. Instantiate **PreprocessRunner** using a pandas Dataframe
    - staticmethods can instantiate **PreprocessRunner** using a .csv or .tab file:
        - `PreprocessRunner.load_from_csv_file(..file path..)`
        - `PreprocessRunner.load_from_tabular_file(..file path..)`
1. Iterate through the columns of the Dataframe
    - Create a **ColumnInfo** object (`column_info.py`) which contains all of the output variables names
      - Pass the **ColumnInfo** object + column data (`pandas.Series`) through these utils:
          - **TypeGuessUtil** (`type_guess_util.py`)
          - **SummaryStatsUtil** (`summary_stats_util.py`)
          - **PlotValuesUtil** (`plot_values.py`)
      - Each of the classes above fills in data within the **ColumnInfo** object

**Example of use:**
 - See `preprocess.py`


## Run tests

```
cd preprocess/code
python -m unittest
```

## Create docs

```
workon preprocess
cd docs
make html
```

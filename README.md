(under initial development)

# raven-metadata-service

Service to produce TwoRavens metadata

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

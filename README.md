[![Build Status](https://travis-ci.org/TwoRavens/raven-metadata-service.svg?branch=master)](https://travis-ci.org/TwoRavens/raven-metadata-service.svg)

---

# raven-metadata-service

Service to produce TwoRavens metadata.

More detailed documentation is available at: https://tworavens.github.io/TwoRavens/Metadata/

## Install

The preprocess library, without the web service, is available via pypi: https://pypi.org/project/tworavens-preprocess/

```pip install tworavens-preprocess```

### Manual install

Prerequisites:
  - python3
  - [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)

Open a Terminal:

```
git clone https://github.com/TwoRavens/raven-metadata-service.git
cd ~/raven-metadata-service
mkvirtualenv preprocess
pip install -r requirements/30_preprocess_web.txt
```

## Usage

### Within Python

Preprocess a single file, write output to screen:

```
from raven_preprocess.preprocess import run_preprocess
run_preprocess('path-to-input-file.csv')
```

Preprocess a single file, write output to file:

```
from raven_preprocess.preprocess import run_preprocess
run_preprocess('path-to-input-file.csv', 'path-to-OUTPUT-file.csv')
```

### Using the wrapper from the manual install

Open a Terminal:

```
cd ~/raven-metadata-service/preprocess/raven_preprocess
workon preprocess
```

Preprocess a single file, write output to screen:

```python preprocess.py [input file]```

Example:

```python preprocess.py ../../test_data/fearonLaitin.csv```

Preprocess a single file, write output to file:

```python preprocess.py [input file name] [output file]```

Example:

```python preprocess.py ../../test_data/fearonLaitin.csv /tmp/fearonLaitin.json```

Both ways accept an --old-format flag which will convert the output to be the same as that available on Harvard Dataverse.

```python preprocess.py ../../test_data/fearonLaitin.csv --old-format```

More examples can be found in the [documentation](https://tworavens.github.io/TwoRavens/Metadata/).

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

## Code of Conduct

...

## License

Apache 2.0

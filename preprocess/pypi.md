
# Steps for making the tworavens-preprocess package

- reference: https://packaging.python.org/tutorials/packaging-projects/

```
# from the top directory:
#
pip install setuptools wheel twine

# build packages
#
python setup.py sdist bdist_wheel

# upload
#
python -m twine upload --verbose  dist/*
```


# Steps for making the tworavens-preprocess package

- reference: https://packaging.python.org/tutorials/packaging-projects/

```
# from the repository's top directory:
#

# install setup tools
#
pip install setuptools wheel twine

# Open/Edit /preprocess/setup.py
# - Update any necessary information
# - Example: "version"

# build packages
#
cd preprocess
rm -rf dist/*
python setup.py sdist bdist_wheel

# upload
#
python -m twine upload --verbose  dist/*
```

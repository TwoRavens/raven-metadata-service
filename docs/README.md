DEPRECATED - DOCS MOVED TO https://tworavens.github.io/TwoRavens/Metadata/


# Document generation

## Public view

The latest docs are available here: http://two-ravens-metadata-service.readthedocs.io/en/latest/

Any updates to the document files pushed to master will show up on the readtheeocs.io site.  There is a TwoRavens service account for readthedocs.io.  Check with @raprasad for creds.

## Development

### Prerequisites

This assumes that a virtualenv has already been created via  [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html).

If you have virtualenvwrapper, the requirements may be installed from the top level of the repository via:

```
# example.  from (your path)/raven-metadata-service/
mkvirtualenv preprocess
pip install -r requirements/30_preprocess_web.txt
```


### Generating HTML from .rst

1. Open a Terminal
1. Go to the top level of the `raven-metadata-service` codebase
1. Run the following:
  ```
  workon preprocess
  cd docs
  make html
  ```
1. Open the output generated in: `raven-metadata-service/docs/build/html`
    - e.g. open the `index.html` in a browser

### Editing the .rst file

Example:
1. Edit the metadata variable descriptions in `docs/source/preprocess_file_description.rst`
1. Re-run [Generating HTML from .rst](#generating-html-from-rst) in the step above
   - View the updates in the HTML

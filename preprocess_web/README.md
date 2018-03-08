
# Initial setup

## Install redis

- [homebrew example](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)

## Create a virtualenv

These instructions assume [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html) is installed.

```
# Do this from the top directory, e.g. within `raven-metadata-service`
mkvirtualenv metadata
pip install -r requirements/30_preprocess_web.txt
```

## Open three Terminals

For each of these windows, 1st `cd` into `raven-metadata-service`

- Terminal 1 - Run Redis

```
cd preprocess_web/code
workon metadata
fab run_redis
```

- Terminal 2 - Run Celery

```
cd preprocess_web/code
workon metadata
fab run_celery
```

- Terminal 3 - Run Web Server

```
cd preprocess_web/code
workon metadata
fab run_web
```

## File upload

- Try this page:
  - http://127.0.0.1:8000/preprocess/form-basic-upload
  - Refresh the response after the file is uploaded

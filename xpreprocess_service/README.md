### future home of queuing service for preprocess

### Dev Set-up

1. Install python3, virtualenvwrapper, redis
2. Create a virtualenv and install requirements
    ```
    # find your python 3.  example output: "/usr/local/bin/python3"
    #
    which python3

    # create a virtual env using the output from above
    #
    mkvirtualenv --python=[output from above] metadata
    # e.g. "mkvirtualenv --python=/usr/local/bin/python3 python3"

    # install requirements
    #
    pip install -r requirements/20_preprocess_service.txt
    ```

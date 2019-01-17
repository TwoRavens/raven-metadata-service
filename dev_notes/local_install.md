# TwoRavens Metadata Service

The TwoRavens metadata service takes a data file as an input and creates a JSON document containing summary statistics.  
  - input: data file (.csv, .tab)
  - output: json document containing summary statistics
    - Based on JSON schema described ...

## Local Setup

The fully running system consists of 4 running pieces:

1. Django web server
1. Celery queue
1. Redis
1. webpack running via npm

To set this up in a development environment please use the instructions below.

### Get the repository

- Use Github Desktop to pull down the [repository](https://github.com/TwoRavens/ravens-metadata-service)
- Alternately, use the command line:
    ```
    git clone https://github.com/TwoRavens/ravens-metadata-service.git

    ```
- From the command line, install the [TwoRavens common](https://github.com/TwoRavens/common) sub repository
    ```
    # cd into the top level of the `ravens-metadata-service` repository
    #
    cd preprocess_web/code
    git submodule add --force -b master https://github.com/TwoRavens/common.git assets/common
    git submodule init
    git submodule update --remote
    ```

### Install virtualenvwrapper

This section requires that you have python 3.6+ on your machine.  

- Install [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)
- Set the shell/Terminal to use virtualenvwrapper.
  - For Mac users:
    1. Open a new terminal
    2. Open your ```~/.bash_profile``` for editing
      - If you don't have a ```~/.bash_profile``` file, then create it
    3. Add these lines
        ```
        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
        source /usr/local/bin/virtualenvwrapper.sh
        ```
    4. Reference: http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file

  - For Ubuntu users:
    1. Open a new terminal
    2. Open your ```~/.bashrc``` for editing
    3. Add these lines
       ```
       export WORKON_HOME=$HOME/.virtualenvs
       export PROJECT_HOME=$HOME/Devel
       VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
       source ~/.local/bin/virtualenvwrapper.sh
       ```
    4. You may need to install virtualenv:
       ```
       sudo apt install virtualenv
       ```
    5. Start new terminals to reload .bashrc


### Make a virtualenv and install requirements

- From the Terminal and within the `ravens-metadata-service` repository.
- Run the following commands (May take a couple of minutes)

  ```
  mkvirtualenv --python=`which python3` metadata  
  pip install -r requirements/30_preprocess_web.txt  
  # note: within the virtualenv, pip defaults to pip3
  ```

- Ubuntu note: If you get the error `OSError: mysql_config not found`, then run  
`sudo apt-get install libmysqlclient-dev`
- Mac note: If you run into Xcode (or other errors) when running the install, google it.  
- Sometimes the [Xcode license agreement hasn't been accepted](http://stackoverflow.com/questions/26197347/agreeing-to-the-xcode-ios-license-requires-admin-privileges-please-re-run-as-r/26197363#26197363)

### Configure your virtualenv

* Edit the [```postactivate``` script for the virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/scripts.html#postactivate).

  - Note: `atom` below may be any text editor
      ```
      atom $VIRTUAL_ENV/bin/postactivate
      ```

* Add this line to the end of the `postactivate` file and save the file
    ```
    export DJANGO_SETTINGS_MODULE=ravens_metadata.settings.local_settings
    ```

* Test the `postactivate` script from your open Terminal:
    ```
    deactivate
    workon metadata
    echo $DJANGO_SETTINGS_MODULE
    ```

- You should see `ravens_metadata.settings.local_settings`

### Test the Django setup

From the top of the `ravens-metadata-service` directory, run:
    ```
    cd preprocess_web/code
    fab init_db
    ```
If no errors are shown, you should be ok and a test sqlite database will have been created.

### Install node

From the top of the `ravens-metadata-service` directory, run:
    ```
    cd preprocess_web/code
    npm install
    ```

### Install Redis

- Install Redis
      - Mac example: https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298

### Run the system!

(There are also scripts to do this--this is the long way.)

1. Open 3 Terminals.  
1. Within each one:
    ```
    cd ~/ravens-metadata-service/preprocess_web/code
    workon metadata
    ```
1. Next, run these commands`
  - Terminal 1: `fab redis_run`
  - Terminal 2: `fab celery_run`
  - Terminal 3: `fab run_web`
    - This last window runs both the django test server and webpack
1. Go to http://127.0.0.1:8080/


### Alternate: Run via the command line

1. Open a Terminal
1. Start the environment
    ```
    cd ~/ravens-metadata-service/preprocess_web/code
    workon metadata

    # -------------------------
    # Preprocess a single file,
    # Write output to screen
    #
    # > fab run_preprocess:[input file name]
    # -------------------------

    # Example:
    fab run_preprocess:../../test_data/fearonLaitin.csv

    # -------------------------
    # Preprocess a single file,
    # Write output to file
    #
    # > fab run_preprocess:[input file name],[output file]
    # -------------------------

    # Example:
    fab run_preprocess:../../test_data/fearonLaitin.csv,/tmp/fearonLaitin.json

    ```

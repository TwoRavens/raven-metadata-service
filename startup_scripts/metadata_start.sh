#!/bin/bash

# -----------------------------------
# (20) Initialize database
#   - Executes if files are located
#     in a different directory
# -----------------------------------
printf "\n(10) Run Init Steps"
fab init-db
fab collectstatic

# -----------------------------------
# (30) "Run web server.."
# -----------------------------------
printf "\n(30) Run web server.."
#setsid python manage.py runserver 0.0.0.0:8080
gunicorn --timeout 120 --workers 3 --bind 0.0.0.0:8080 ravens_metadata.wsgi_preprocess_gce

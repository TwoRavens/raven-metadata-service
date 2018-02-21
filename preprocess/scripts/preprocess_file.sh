#!/bin/bash

# -------------------------------
# Run Preprocess for a single file
# -------------------------------
printf "\n----------------------"
printf "\nTwoRavens: preprocess"
printf "\n----------------------\n"
cd /var/apps/raven-metadata-service/preprocess/code
#cd /Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess/code
python preprocess.py $@

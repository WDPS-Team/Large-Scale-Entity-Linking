#!/bin/bash

echo "Building virtual environment"
rm -rf venv/*
rm -rf venv.zip
pip3 install --user virtualenv
python3 /usr/local/lib/python3.5/dist-packages/virtualenv.py -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_md
virtualenv --relocatable venv
zip -r venv.zip venv
deactivate

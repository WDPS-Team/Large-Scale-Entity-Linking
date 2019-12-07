#!/bin/bash

echo "Building virtual environment"
rm -rf venv/*
rm -rf venv.zip
pip3 install --user virtualenv
python3 /usr/local/lib/python3.5/dist-packages/virtualenv.py -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m nltk.downloader stopwords -d venv/nltk_data
python3 -m nltk.downloader punkt -d venv/nltk_data
python3 -m nltk.downloader wordnet -d venv/nltk_data
pip3 install /en_core_web_md-2.2.5.tar.gz
pip3 install /en_core_web_lg-2.2.5.tar.gz
virtualenv --relocatable venv
zip -r venv.zip venv
deactivate

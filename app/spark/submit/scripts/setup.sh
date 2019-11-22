#!/bin/bash

(cd /app/src  && python3 -m venv ./venv)
source "/app/src/venv/bin/activate"
pip3 install virtualenv
pip3 install --user virtualenv -r /app/src/requirements.txt

virtualenv --relocatable /app/src/venv
deactivate
zip -qr /app/src/venv.zip /app/src/venv

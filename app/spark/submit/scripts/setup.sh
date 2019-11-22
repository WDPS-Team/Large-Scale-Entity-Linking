#!/bin/bash

(cd /app/src  && python3 -m venv ./venv)

(cd /app/src && pip3 install --user virtualenv -r requirements.txt)

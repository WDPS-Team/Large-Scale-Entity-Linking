#!/bin/bash

(cd /app/src  && python3 -m venv ./venv)
(cd /app/src  && python3 -m pip install --user virtualenv -r requirements.txt)

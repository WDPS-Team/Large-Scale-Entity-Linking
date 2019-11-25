#!/bin/bash

source "/app/src/venv/bin/activate"
cp /app/data/sample.warc.gz /sample.warc.gz
pyfileslist=$(ls -p /app/src/*.py | grep -v / | tr '\n' ',')

/spark/bin/spark-submit --files /sample.warc.gz /app/src/spark_main.py --py-files "$pyfileslist"

deactivate
rm -r /app/data/predictions.tsv
cp -r /output/predictions.tsv/ /app/data/predictions.tsv

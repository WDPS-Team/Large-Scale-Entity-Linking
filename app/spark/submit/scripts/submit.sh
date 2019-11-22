#!/bin/bash

# source venv/bin/activate
# virtualenv --relocatable venv
zip -r /venv.zip /app/src/venv

cp /app/data/sample.warc.gz /sample.warc.gz

/spark/bin/spark-submit /app/src/spark_main.py --files /sample.warc.gz --archives venv.zip#VENV

rm -r /app/data/predictions.tsv
cp -r /output/predictions.tsv/ /app/data/predictions.tsv

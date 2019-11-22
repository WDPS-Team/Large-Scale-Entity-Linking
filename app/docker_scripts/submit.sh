#!/bin/bash

cp /app/data/sample.warc.gz /sample.warc.gz

/spark/bin/spark-submit /app/src/spark_main.py --files /sample.warc.gz

rm -r /app/data/predictions.tsv
cp -r /output/predictions.tsv/ /app/data/predictions.tsv

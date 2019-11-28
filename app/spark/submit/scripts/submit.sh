#!/bin/bash

cp /app/data/sample.warc.gz /sample.warc.gz

source /app/src/venv/bin/activate
#--master spark-master \
#  --conf spark.pyspark.virtualenv.enabled=true \
#  --conf spark.pyspark.virtualenv.type=native \
#  --conf spark.pyspark.virtualenv.requirements=/app/src/requirements.txt \
#  --conf spark.pyspark.virtualenv.bin.path=/app/src/venv/bin \

/spark/bin/spark-submit \
  --files /sample.warc.gz \
  /app/src/spark_main.py

deactivate
rm -r /app/data/predictions.tsv
cp -r /output/predictions.tsv/ /app/data/predictions.tsv

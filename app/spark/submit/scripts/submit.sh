#!/bin/bash

pip3 install -r /app/src/requirements.txt


cp /app/data/sample.warc.gz /sample.warc.gz

# --master spark://spark-master:7077
/spark/bin/spark-submit --files /sample.warc.gz /app/src/spark_main.py 
#  --conf spark.pyspark.virtualenv.enabled=true \
# --conf spark.pyspark.virtualenv.type=native \
# --conf spark.pyspark.virtualenv.requirements=/app/src/requirements.txt \
# --conf spark.pyspark.virtualenv.bin.path=/app/src/venv  \
# --conf spark.pyspark.python=/app/src/venv/bin/python3 \
# spark-submit --master yarn-client --conf spark.pyspark.virtualenv.enabled=true  --conf spark.pyspark.virtualenv.type=native --conf spark.pyspark.virtualenv.requirements=/Users/jzhang/github/spark/requirements.txt --conf spark.pyspark.virtualenv.bin.path=/Users/jzhang/anaconda/bin/virtualenv --conf spark.pyspark.python=/usr/local/bin/python3 spark_virtualenv.py

rm -r /app/data/predictions.tsv
cp -r /output/predictions.tsv/ /app/data/predictions.tsv

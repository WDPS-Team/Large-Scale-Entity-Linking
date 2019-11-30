#!/bin/bash
#rm -r /output/predictions.tsv
cp /data/sample.warc.gz /sample.warc.gz

source venv/bin/activate
# Run Spark Job
PYSPARK_PYTHON=$(readlink -f $(which python3)) /spark/bin/spark-submit \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=venv/bin/virtualenv \
src/spark.py --es "es01:9200" --f "sample.warc.gz"

deactivate
rm -r /data/output/
cp -r /output/ /data/output/

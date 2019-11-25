# TODOS:
# Add parameters for input and output files

# Prerequsites:
# - setup DAS4 cluster

# Cleanup Files
rm ./output.tsv
hdfs dfs -rm -r output/predictions.tsv

# PYSPARK_PYTHON=$(readlink -f $(which python3)) /home/bbkruit/spark-2.1.2-bin-without-hadoop/bin/spark-submit \
# --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
# --master yarn \
# --archives venv.zip#VENV \
# app/src/spark.py app/data/sample.warc.gz ./log

# PYSPARK_PYTHON=$(readlink -f $(which python3)) /local/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
# --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
# --master yarn \
# --archives venv.zip#VENV \
# app/src/spark.py

PYSPARK_PYTHON=$(readlink -f $(which python3)) /local/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=venv/bin/virtualenv \
app/src/spark.py


# Copying Output File from HDFS
hdfs dfs -copyToLocal output/predictions.tsv/part-00000 ./output.tsv

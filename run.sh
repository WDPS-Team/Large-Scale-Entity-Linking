# Delete output files prior run
rm ./output.tsv
hdfs dfs -rm -r output/predictions.tsv

source venv/bin/activate
# Run Spark Job
PYSPARK_PYTHON=$(readlink -f $(which python3)) /local/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=venv/bin/virtualenv \
app/src/spark.py $ES_NODE:$ES_PORT

deactivate
# Copying Output File from HDFS
hdfs dfs -copyToLocal output/predictions.tsv/part-00000 ./output.tsv

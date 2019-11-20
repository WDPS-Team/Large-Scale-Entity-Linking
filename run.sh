# TODOS:
# Add parameters for input and output files

# Prerequsites:
# - setup DAS4 cluster

# General setup
echo "Copying input file to hdfs"
hdfs dfs -copyFromLocal ./app/data/sample.warc.gz hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz
if [ $? -eq 0 ]
then
  echo "input data copied, running program"
else
  echo "something went wrong"
  exit 1
fi

# Cleanup Files
rm ./output.tsv
hdfs dfs -rm -r output/predictions.tsv

# Starting Spark on yarn
/local/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit --master yarn ./app/src/spark_main.py

# Copying Output File from HDFS
hdfs dfs -copyToLocal output/predictions.tsv/part-00000 ./output.tsv

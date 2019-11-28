#Delete output files prior run
rm ./output.tsv
hdfs dfs -rm -r output/predictions.tsv

#checking for input file
if [ "$#" -ne 2 ]
then
    echo "Correct Usage: ./run.sh \$ES_PATH <input_file>"
   exit 1
else
   #move file to hdfs if it exists
   if [ -f $2 ]; then
        echo "Copying input file"
        hdfs dfs -copyFromLocal $2 "input.warc.gz"  #TODO: avoid renaming of file to input.warc.gz and pass the file as a parameter to spark job
    else
        echo "File $2 does not exist."
        exit 1
    fi
fi


source venv/bin/activate
# Run Spark Job
PYSPARK_PYTHON=./VENV/venv/bin/python3 ../spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--master yarn \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=./VENV/venv/bin/virtualenv \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
--archives venv.zip#VENV \
src/spark.py --es "$1"

deactivate
# Copying Output File from HDFS
hdfs dfs -copyToLocal output/predictions.tsv/part-00000 ./output.tsv

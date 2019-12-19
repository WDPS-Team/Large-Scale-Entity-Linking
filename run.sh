#!/bin/bash

# default input values
ES_PATH=`cat .es_path`
INPUT_PATH="data/sample.warc.gz"
OUTPUT_FILE="output.tsv"

# check for custom input parameters
while [[ $# -gt 0 ]]
do
case $1 in
    -es)
    ES_PATH="$2"
    shift
    shift
    ;;
    -f)
    INPUT_PATH="$2"
    shift
    shift
    ;;
    -o)
    OUTPUT_FILE="$2"
    shift
    shift
    ;;
esac
done

#move file to hdfs if it exists
if [ -f $INPUT_PATH ]; then
    echo "Copying input file: $INPUT_PATH"
    INPUT_FILE=`basename $INPUT_PATH`
    FULL_INPUT_PATH="$(basename $PWD)/$INPUT_FILE"
    hdfs dfs -mkdir -p `basename $PWD`
    hdfs dfs -copyFromLocal -p $INPUT_PATH $FULL_INPUT_PATH
    echo "Copied Input To HDFS $FULL_INPUT_PATH"
else
    echo "ERROR: $INPUT_PATH does not exist."
    exit 1
fi

#Elastic search server check
response=$(curl --write-out %{http_code} --silent --output /dev/null $"$ES_PATH/freebase")
if [ $response -ne 200 ] || [ -z $ES_PATH ] ; then
    echo "ERROR: Elastic Search on node $ES_PATH is not running."
    exit 1
fi

#Delete output files prior run
rm $OUTPUT_FILE
rm -rf tmp
mkdir tmp
HDFS_TMP_OUTPUT="$(basename $PWD)/output"
hdfs dfs -rm -r $HDFS_TMP_OUTPUT

# submit spark job
prun -v -1 -np 1 -t 21600 sh spark_submit.sh $ES_PATH $FULL_INPUT_PATH $HDFS_TMP_OUTPUT

# Copying Output File from HDFS
hdfs dfs -get "$HDFS_TMP_OUTPUT/predictions.tsv/*" tmp/
cat tmp/* > $OUTPUT_FILE

#Deleting copied input file from HDFS
hdfs dfs -rm -r $FULL_INPUT_PATH > /dev/null

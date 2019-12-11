#!/bin/bash

#default values
ES_PATH=`cat .es_path`
KB_PATH=`cat .kb_path`
INPUT_PATH="data/sample.warc.gz"
OUTPUT_FILE="output.tsv"

# check for input parameters
while [[ $# -gt 0 ]]
do
case $1 in
    -es)
    ES_PATH="$2"
    shift
    shift
    ;;
    -kb)
    KB_PATH="$2"
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
    hdfs dfs -copyFromLocal $INPUT_PATH $INPUT_FILE
else
    echo "ERROR: $INPUT_PATH does not exist."
    exit 1
fi

#Elastic search server check
response=$(curl --write-out %{http_code} --silent --output /dev/null $"$ES_PATH/freebase/label")
if [ $response -ne 200 ] || [ -z $ES_PATH ] ; then
    echo "ERROR: Elastic Search on node $ES_PATH is not running."
    exit 1
fi

#Trident server check
response=$(curl --write-out %{http_code} --silent --output /dev/null $KB_PATH)
if [ $response -ne 200 ] || [ -z $KB_PATH ] ; then
    echo "ERROR: Trident on node $KB_PATH is not running."
    exit 1
fi

#Delete output files prior run
rm $OUTPUT_FILE
rm -rf tmp
mkdir tmp
hdfs dfs -rm -r output

# submit spark job
prun -v -1 -np 1 -t 3600 sh run_das.sh $ES_PATH $INPUT_FILE $KB_PATH

# Copying Output File from HDFS
hdfs dfs -get output/predictions.tsv/* tmp/
cat tmp/* > $OUTPUT_FILE

#copying all intermediate files for debugging
#hdfs dfs -copyToLocal output/* ./tmp/   

#Deleting copied input file from HDFS
hdfs dfs -rm -r $INPUT_FILE > /dev/null

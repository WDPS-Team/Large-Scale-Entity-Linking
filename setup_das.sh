#!/bin/bash

echo "Loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ]; then echo "All done loading prun"; else echo "Error in loading prun" && exit 1; fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ]; then echo "All done loading hadoop"; else echo "Error in loading Hadoop" && exit 1; fi
module load python/3.6.0
if [ $? -eq 0 ]; then echo "All done loading python3.6"; else echo "Error in loading Python" && exit 1; fi

if [ ! -d "/home/wdps1936/elasticsearch-2.4.1" ]; then
    echo "Copying Elastic Search folder"
    cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1
fi

if [ ! -d "/home/wdps1936/spark" ]; then
    echo "Copying Spark Framework folder"
    cp -r /local/spark /home/wdps1936/
fi

prun -v -np 1 sh setup_venv.sh

echo "Copying default input file to hdfs"
hdfs dfs -rm -r hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz
hdfs dfs -copyFromLocal -f ./app/data/sample.warc.gz hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz

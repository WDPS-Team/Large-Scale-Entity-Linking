#!/bin/bash

echo "Loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ]; then echo "All done loading prun"; else echo "Error in loading prun" && exit 1; fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ]; then echo "All done loading hadoop"; else echo "Error in loading Hadoop" && exit 1; fi
module load python/3.6.0
if [ $? -eq 0 ]; then echo "All done loading python3.6"; else echo "Error in loading Python" && exit 1; fi

echo "Setting up Elastic Search"
if [ ! -d "/home/wdps1936/elasticsearch-2.4.1" ]; then
    echo "Copying Elastic Search folder"
    cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1
fi
source ./start_elasticsearch_server.sh > /dev/null   #ES_NODE and ES_PORT are needed for spark job submission

if [ ! -d "/home/wdps1936/spark" ]; then
    echo "Copying Spark Framework folder"
    cp -r /local/spark /home/wdps1936/
fi

echo "Building virtual environment" #TODO: Don't build venv in headnode
rm -rf venv
rm -rf venv.zip
pip3 install --user virtualenv
python3 ~/.local/lib/python3.6/site-packages/virtualenv.py -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
virtualenv --relocatable venv
zip -r venv.zip venv
deactivate

echo "Copying default input file to hdfs"
hdfs dfs -rm -r hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz
hdfs dfs -copyFromLocal -f ./app/data/sample.warc.gz hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz

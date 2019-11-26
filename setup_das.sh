#!/bin/bash

echo "loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ]; then echo "all done loading prun"; else echo "something went wrong" && exit 1; fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ]; then echo "all done loading hadoop"; else echo "something went wrong" && exit 1; fi
module load python/3.6.0
if [ $? -eq 0 ]; then echo "all done loading python3.6"; else echo "something went wrong" && exit 1; fi

echo "copy binaries"
# cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1

# Install python
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

echo "Copying defailt input file to hdfs"
hdfs dfs -rm -r hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz
hdfs dfs -copyFromLocal -f ./app/data/sample.warc.gz hdfs://master.ib.cluster:8020/user/wdps1936/sample.warc.gz

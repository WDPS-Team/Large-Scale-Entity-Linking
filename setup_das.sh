#!/bin/bash

echo "loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ]; then echo "all done loading prun"; else echo "something went wrong" && exit 1; fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ]; then echo "all done loading hadoop"; else echo "something went wrong" && exit 1; fi
module load python/3.5.2
if [ $? -eq 0 ]; then echo "all done loading python3.6"; else echo "something went wrong" && exit 1; fi

echo "copy binaries"
cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1

# Install python
rm -rf venv
virtualenv venv --python=/cm/shared/package/python/3.5.2/bin/python3
source "venv/bin/activate"
pip3 install -r app/src/requirements.txt
python3 -m spacy download en_core_web_sm
deactivate

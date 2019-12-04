#!/bin/bash

echo "Loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ]; then echo "All done loading prun"; else echo "Error in loading prun" && exit 1; fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ]; then echo "All done loading hadoop"; else echo "Error in loading Hadoop" && exit 1; fi
module load python/3.6.0    # Load python 3.6.0
if [ $? -eq 0 ]; then echo "All done loading python3.6"; else echo "Error in loading Python" && exit 1; fi

if [ ! -d "/home/wdps1936/elasticsearch-2.4.1" ]; then
    echo "Copying Elastic Search folder"
    cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1
fi

if [ ! -d "/home/wdps1936/trident" ]; then
    echo "Copying Trident folder"
    cp -r /home/jurbani/trident /home/wdps1936/trident
fi

# Build venv in cluster node
prun -v -np 1 sh setup_venv.sh

#!/bin/bash

echo "loading binaries"
module load prun # DAS4 instance management
if [ $? -eq 0 ] then echo "all done loading prun" else echo "something went wrong" exit 1 fi
module load hadoop # Hadoop stuff
if [ $? -eq 0 ] then echo "all done loading hadoop" else echo "something went wrong" exit 1 fi

echo "copy binaries"
cp -r /home/jurbani/wdps/elasticsearch-2.4.1 /home/wdps1936/elasticsearch-2.4.1


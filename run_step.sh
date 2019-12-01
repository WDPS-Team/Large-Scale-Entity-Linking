#!/bin/bash

#default values
ES_PATH=`cat .es_path`

#Elastic search server check
response=$(curl --write-out %{http_code} --silent --output /dev/null $ES_PATH)
if [ $response -ne 200 ]
then
    echo "ERROR: Elastic Search on node $ES_PATH is not running."
    exit 1
fi

#submit spark job
prun -v -1 -np 1 sh run_step_das.sh $ES_PATH


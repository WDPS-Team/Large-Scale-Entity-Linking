#checking for input file
if [ "$#" -ne 2 ]
then
    echo "Correct Usage: \$ES_PATH <input_file>"
   exit 1
else
   #move file to hdfs if it exists
   if [ -f $2 ]; then
        echo "Copying input file"
        hdfs dfs -rm -r "input.warc.gz"
        hdfs dfs -copyFromLocal $2 "input.warc.gz"  #TODO: avoid renaming of file to input.warc.gz and pass the file as a parameter to spark job
    else
        echo "File $2 does not exist."
        exit 1
    fi
    #Elastic search server check
    response=$(curl --write-out %{http_code} --silent --output /dev/null $1)
    if [ $response -ne 200 ]
    then
        echo "Elastic Search node $1 is not running."
        exit 1
    fi
fi

#Delete output files prior run
rm output.tsv
hdfs dfs -rm -r output/predictions.tsv

#submit spark job
prun -v -1 -np 1 sh run.sh $1 $2

# Copying Output File from HDFS
hdfs dfs -get output/predictions.tsv/part-00000 ./output.tsv
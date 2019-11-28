ES_PORT="9200"
ES_HOST="localhost"
IFILE="../data/sample-labels-cheat.txt"
python3 es_file_loader.py $ES_HOST $ES_PORT $IFILE

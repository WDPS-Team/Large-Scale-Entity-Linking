PWD_PATH=$(pwd)
SCR_DIR=`basename $PWD_PATH`
SCR_PATH="/var/scratch2/wdps1936/$SCR_DIR"

if [ ! -d "$SCR_PATH/trident" ]; then
    echo "Copying Trident folder"    #copying allows creating multiple instances of Trident
    mkdir -p $SCR_PATH
    cp -r /var/scratch2/wdps1936/trident $SCR_PATH/
fi

KB_PORT=9090
KB_BIN=$SCR_PATH/trident/build/trident
KB_PATH=/home/jurbani/data/motherkb-trident

echo "Lauching an instance of the Trident server on a random node in the cluster ..."
prun -o .kb_log -v -np 1 -t 21600 $KB_BIN server -i $KB_PATH --port $KB_PORT </dev/null 2> .kb_node &
echo "Waiting 5 seconds for trident to set up (use 'preserve -llist' to see if the node has been allocated)"
until [ -n "$KB_NODE" ]; do KB_NODE=$(cat .kb_node | grep '^:' | grep -oP '(node...)'); done
sleep 5
KB_PID=$!
echo "Trident should be running now on node $KB_NODE:$KB_PORT (connected to process $KB_PID)"

echo "$KB_NODE:$KB_PORT" > .kb_path

# python sparql.py $KB_NODE:$KB_PORT "select * where {<http://rdf.freebase.com/ns/m.01cx6d_> ?p ?o} limit 100"

# query="select * where {\
#   ?s <http://www.w3.org/2002/07/owl#sameAs> <http://rdf.freebase.com/ns/m.0k3p> .\
#   ?s <http://www.w3.org/2002/07/owl#sameAs> ?o .}"
# python sparql.py $KB_NODE:$KB_PORT "$query"

# query="select distinct ?abstract where {  \
#   ?s <http://www.w3.org/2002/07/owl#sameAs> <http://rdf.freebase.com/ns/m.0k3p> .  \
#   ?s <http://www.w3.org/2002/07/owl#sameAs> ?o . \
#   ?o <http://dbpedia.org/ontology/abstract> ?abstract . \
# }"
# python sparql.py $KB_NODE:$KB_PORT "$query"

#kill $KB_PID

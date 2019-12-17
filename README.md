# Large Scale Entity Linking

## Description

### Architecture

![image](https://github.com/WDPS-Team/2019-WDPS/blob/architecture/docs/architecture/architectue2.0.png)

- This project is to perform Entity Linking on a collection of web pages using entities from Freebase. 
- The **Input** is a set of pages in WARC format, stored information that crawled from web. The final goal is to link the 'entity mention' in WARCfile to 'entities' in Freebase, and **Output** format is : [Document ID, Entity Mention, Freebase ID] 
- This project consists of following steps: 
    1. WARCSplitReader - Reading and splitting the WARCfile into lines and proccessing in parallel. Filtering the invalid data. 
    2. TextPreprocessor - Cleaning the result from the last step, removing useless and non-essential data (css, ids, tags). Using `beautifulsoup` to extract text data in HTML. And finally reformat the result as split the text into sentences. 
    3. NLPPreprocessor - Processing the sentences with different NLP techniques. In this step we use `nltk` to do the NLP preprocessing. First tokenize these sentences, then lemmatize the tokens, after that remove all stop words in it. Finally combine the words as strings. 
    4. EntityExtractor - We use `spacy` to do the NER part and only extract entities that are in type of `PERSON`,`ORGANIZATION` and `LOCATION`. 
    5. EntityLinker - we use `elasticsearch` to link the mention to all possible candidate entities in Freebase. Then use `LexVec` to calculate cosine similarity between an mention and an candidate entity and sort the result by similarity. 
    6. DataDisambiguator - 
    7.
    
##TODO: to be continued 

## DAS4 Execution

### DAS4 Setup

Run `sh setup.sh` to build virtual environment and download the dependencies.

### Quickrun:

1. `. start_elasticsearch_server.sh` + `./run.sh` will run the latest started elastic search instance and the defaults set in run.sh

### Start Elastic Search Server

1. Run `sh start_elasticsearch_server.sh` to start the Elastic Search server and it will run for 15 minutes by default.
2. The address of the cluster node will be displayed and you can make sure it's running using `curl <ES_NODE>:9200`

### Run Spark Job

`sh run.sh`

By default, `data/sample.warc.gz` will be taken as input and output will be in `output.tsv`. Job submission can be customized using the options -f, -o and -es.
Eg: `sh run.sh -f input.warc.gz -o out.tsv -es node007:9200`


## Local Development

### Prerequsites

Ideally you use Docker for local development (esp. on Windows), thus you need:
- Docker (for Windows/Mac)
- docker-compose

### Setup Local Components:

#### Building Base Image:

1. Execute `docker-compose -f docker-compose.base.yml build` to build the Spark base images.
2. Execute `docker-compose build` to build the relevant images for running the local development.

#### Install Dependencies for Development:

1. `pip3 install elasticsearch==7.1.0` for loading data into Elasticsearch

#### Loading Data into Elastic Search

1. Start Elasticsearch with `docker-compose up es01`
2. Run the following commands (given Python used python3):
    - `python3 load_elasticsearch.py localhost 9200 ./data/sample-labels-cheat.txt`

**Testing Elasticsearch**
Test with `curl "http://localhost:9200/freebase/label/_search?q=obama"`. Expect a freebase id linking to Obama.

#### Load Data into Trident

**Option 1 - Index Data**
1. Download and place KB data (alternatively copy an existing already indexed KB, see option 2)
    - Go to `trident/data`
    - create dir if necessary: `yago2s_input`
    - download yago2s knowledge base [here](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/archive/)
    - extract in `yago2s_input` folder
2. Index the knowledge base with trident
    - Run `docker-compose run trident ./trident load -i /data/kb/trident -f /data/kb/yago2s_input`
    - Notice: You might need to increase the memory size for the Docker VM (Windows + MacOs), was tested with 8192MB on Win10
**Option 2 - Use Already Indexed KB**
1. Copy indexed knowledge base to `trident/data` so that the Trident files are stored under `trident/data/trident`

**Testing the Trident Store**

```
python3 sparql.py localhost:9090 "SELECT DISTINCT ?class WHERE {?s a ?class .} LIMIT 25 OFFSET 0"

python3 sparql.py localhost:9090 "SELECT ?subject ?predicate ?object WHERE {?subject ?predicate ?object} LIMIT 100"
```

### Setup & Handling Spark

#### Setup

- Run `docker-compose run spark-submit /setup.sh`

### Run Spark Job

- Run `docker-compose run spark-submit /submit.sh`

### Reset the Local Development Enviroment

- Run `docker-compose down`, then load data back into Elasticsearch and redo Spark Setup.

### Handy Notes:

- Recursive copy from DAS-4 to local storage:  
  `scp -rp -oProxyJump=PERSONALUSERID@ssh.data.vu.nl USERID@fs0.das4.cs.vu.nl:/filepath ./target/`

- Access DAS4 Cluster from home:   
   `ssh -L22022:fs0.das4.cs.vu.nl:22 -oProxyJump=<VUNET_ID>@ssh.data.vu.nl <GROUP_ID>@fs0.das4.cs.vu.nl`
   Use `ssh://<DAS4_ID>@localhost:22022/` to mount in your file system.

- Access Elastic Search from home:
    `ssh -L9200:<ES_NODE>:9200 -oProxyJump=<VUNET_ID>@ssh.data.vu.nl <DAS4_ID>@fs0.das4.cs.vu.nl`
    
- Access Spark UI from home:
    `ssh -L8080:fs0.das4.cs.vu.nl:8088 -oProxyJump=<VUNET_ID>@ssh.data.vu.nl <DAS4_ID>@fs0.das4.cs.vu.nl`
    Now Spark UI should be accessible via `localhost:8080`
- Query Trident on local:
    `python3 sparql.py 'localhost:9090' "select * where {<http://rdf.freebase.com/ns/m.0d0xs> ?p ?o} limit 1000"`


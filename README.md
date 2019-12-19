# Large Scale Entity Linking

## Table Of Contents

[1. Motivation](#1-motivation)  
[2. Our Solution](#2-our-solution)  
[2.1. Architecture Overview](#21-architecture-overview)  
[2.2. WARC Reading](#22-warc-reading)  
[2.3. Text Extraction](#23-text-extraction)  
[2.4. Entity Linking](#24-entity-linking)  
[2.4.1 Candidate Generation](#241-candidate-generation)  
[2.4.2 Candidate Ranking](#242-candidate-ranking)  
[2.4.3 Mapping Selection](#243-mapping-selection)  
[2.5. Output Write](#25-output-write)  
[3. DAS4 Execution](#3-das4-execution)  

## 1. Motivation

## 2. Our Solution

### 2.1. Architecture Overview

![image](/docs/overview.svg)

### 2.2. WARC Reading
### 2.3. Text Extraction
### 2.4. Entity Linking
#### 2.4.1 Candidate Generation
#### 2.4.2 Candidate Ranking
#### 2.4.3 Mapping Selection
### 2.5. Output Write

## 3. DAS4 Execution

### Prerequisistes

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


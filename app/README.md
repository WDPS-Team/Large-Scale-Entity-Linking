# App

Run everything in the `app` folder.

## Setup Development Enviroment

1. `docker-compose build` to load images and build dependet images.
2. Load the Trident store
    1. Setup Input data
         - go to `app/trident-data`
         - create dir if necessary: `yago2s_input`
         - download yago2s knowledge base [here](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/archive/)
         - extract in `yago2s_input` folder
    2. Index the knowledge base with trident
        - run `docker-compose run trident ./trident load -i /data/kb/trident -f /data/kb/yago2s_input`
        - Notice: You might need to increase the memory size for the Docker VM (Windows + MacOs), was tested with 8192MB on Win10
3. `docker-compose up`
4. Test the Trident Store
   - On Windows:

      ```powershell
      $KB_NODE="localhost"
      $KB_PORT="9090"

      $query = " SELECT DISTINCT ?class
      WHERE {
        ?s a ?class .
      }
      LIMIT 25
      OFFSET 0"
      python sparql.py ${KB_NODE}:${KB_PORT} "$query"

      $query = "SELECT ?subject ?predicate ?object
          WHERE {?subject ?predicate ?object} 
          LIMIT 100"
      python sparql.py ${KB_NODE}:${KB_PORT} "$query"
      ```
5. Load the Elastic Search Data:
   1. Run `./elasticsearch/load_sample_data.sh` to load all data
6. Test Elastic Search Instance with `curl "http://localhost:9200/freebase/label/_search?q=obama"`

## Run Spark Jobs

### Run a Python application on dockerized Spark standalone cluster

```shell
docker-compose run spark-submit sh /submit.sh
```

### Warc Splitting, Entity Extraction and Entity Linking
Steps 1 to 3 of main architecture

#### Requirements
    warcio==1.7.1
    lxml==4.4.1
    nltk==3.4.5
    spacy==2.2.2

Or run `pip3 install --user -r requirements.txt`

#### Configuration
    python3 -m spacy download en_core_web_sm
    python3 -m spacy download en
    python3 config.py

#### Execution
    python3 WARCSplitReader.py <INPUT_WARC_FILE> <OUTPUT_FOLDER>
    python3 EntityExtractor.py <FOLDER>
    python3 EntityLinker.py <ENTITY>

### Run Spark Jobs on DAS4

Probably need to use yarn?

## Utils

- Recursive copy from DAS-4 to local storage:  
  `scp -rp -oProxyJump=PERSONALUSERID@ssh.data.vu.nl USERID@fs0.das4.cs.vu.nl:/filepath ./target/`

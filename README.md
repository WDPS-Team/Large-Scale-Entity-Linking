# 2019-WDPS

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

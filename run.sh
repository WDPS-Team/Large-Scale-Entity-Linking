source venv/bin/activate

# Run Spark Job
PYSPARK_PYTHON=./VENV/venv/bin/python3 /local/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--master yarn \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=./VENV/venv/bin/virtualenv \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
--archives venv.zip#VENV \
src/spark.py --es "$1"

deactivate
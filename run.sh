source venv/bin/activate

# Run Spark Job
PYSPARK_PYTHON=python3 ../spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=venv/bin/virtualenv \
src/spark.py --es "$1"

deactivate
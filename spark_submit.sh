source venv/bin/activate

# Run Spark Job
PYSPARK_PYTHON=./VENV/venv/bin/python3 ../spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--master yarn \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=./VENV/venv/bin/virtualenv \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
--conf spark.executor.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64 \
--conf spark.driver.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64 \
--conf spark.yarn.am.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64 \
--num-executors 38 --executor-cores 2 --executor-memory 6GB \
--archives venv.zip#VENV \
--py-files src/LexVec.py \
src/spark.py --es "$1" --f "$2" --kb "$3" --hdfsout "$4"

deactivate

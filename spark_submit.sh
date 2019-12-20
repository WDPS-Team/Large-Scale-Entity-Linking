source venv/bin/activate

# Run Spark Job
PYSPARK_PYTHON=./VENV/venv/bin/python3 PYTHONPATH=./VENV/venv/build-python /var/scratch2/wdps1936/spark/spark-2.4.0-bin-hadoop2.7/bin/spark-submit \
--master yarn \
--conf spark.pyspark.virtualenv.enabled=true \
--conf spark.pyspark.virtualenv.type=native \
--conf spark.pyspark.virtualenv.requirements=requirements.txt \
--conf spark.pyspark.virtualenv.bin.path=./VENV/venv/bin/virtualenv \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=./VENV/venv/bin/python \
--conf spark.yarn.appMasterEnv.PYTHONPATH=./VENV/venv/build-python \
--conf spark.executor.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64:/cm/shared/package/python/3.5.2/lib \
--conf spark.driver.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64:/cm/shared/package/python/3.5.2/lib \
--conf spark.yarn.am.extraLibraryPath=/cm/shared/package/gcc/6.4.0/lib64:/cm/shared/package/python/3.5.2/lib \
--num-executors 12 --executor-cores 5 --executor-memory 24GB \
--archives venv.zip#VENV \
--py-files src/LexVec.py,src/ELCandidateRanking.py \
src/spark.py --es "$1" --f "$2" --hdfsout "$3"

deactivate

from pyspark import SparkContext, SparkFiles

# Initialize Spark App
sc = SparkContext()

# Read the input file as a rdd
input_file = sc.textFile("sample.warc.gz")
# Space for the main program


# TODO: Convert RDD into a TSV

# Write the file to hdfs
output_rdd = input_file
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv")
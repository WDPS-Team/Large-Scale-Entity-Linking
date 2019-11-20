from pyspark import SparkContext, SparkFiles

# Initialize Spark App
sc = SparkContext()

# Read the input file as a rdd
input_file = sc.textFile("sample.warc.gz")
# Space for the main program



# Write the file to hdfs
input_file.saveAsTextFile("wdps1936output")
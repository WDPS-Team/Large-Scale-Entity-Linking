from pyspark import SparkContext, SparkFiles

sc = SparkContext()

file1 = sc.textFile("app/data/sample.warc.gz")
everything = file1.collect()

# Write the entire file to the local file system
file = open("/app/src/output", "w+")
file.write(str(everything))
file.close()

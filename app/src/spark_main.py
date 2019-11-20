from pyspark import SparkContext, SparkFiles

# Initialize Spark App
sc = SparkContext()

# Read the input file as a rdd
input_file = sc.textFile("app/data/sample.warc.gz")
# Space for the main program



# Write the entire file to the local file system
everything = input_file.collect()
file = open("output", "w+")
file.write(str(everything))
file.close()

from pyspark import SparkContext, SparkFiles


class WARCSplitReader:

    def __init__(self, spark_session, lines_of_input_file):
        self.sc = spark_session
        self.raw_lines = lines_of_input_file
        self.docs = None

    def __split_records(self):
        payload = ''
        for line in self.raw_lines:
            if line.strip() == "WARC/1.0":
                yield payload
                payload = ''
            else:
                payload += " " + line

    def convert_to_docs(self):
        self.docs = self.__split_records()
        return self.sc.parallelize(self.docs)

# Initialize Spark App
sc = SparkContext()

# Read the input file as a rdd
input_file = sc.textFile("sample.warc.gz")
# Space for the main program

wsr = WARCSplitReader(sc, input_file.collect())
docs_rdd = wsr.convert_to_docs()

# TODO: Convert RDD into a TSV

# Write the file to hdfs
output_rdd = docs_rdd
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv")

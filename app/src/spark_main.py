from pyspark import SparkContext, SparkFiles
import spacy
import config
from WARCSplitReader import WARCSplitReader

# Initialize Spark App
sc = SparkContext()

print("using versions")
print("spacy: {0}".format(spacy.__version__))
print(config.WARC_ID)

# Read the input file as a rdd
input_file = sc.textFile("sample.warc.gz")
# Space for the main program

wsr = WARCSplitReader(sc, input_file.collect())

docs_rdd = wsr.parse_warc_records()
docs_rdd = wsr.process_warc_records()
wsr.filter_invalid_records()
docs_rdd = wsr.clean_warc_responses()
print("row count: {0}".format(docs_rdd.count()))

# TODO: Convert RDD into a TSV

# Write the file to hdfs
output_rdd = docs_rdd
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv")

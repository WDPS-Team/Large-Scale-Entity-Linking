from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
from EntityExtractor import EntityExtractor

# Initialize Spark App
sc = SparkContext()

# STAGE 1 - INPUT READING
# -> READ warc files in a distributed manner
# -> Clean all warc records (js, style) with lxml
input_file = sc.textFile("sample.warc.gz")
wsr = WARCSplitReader(sc, input_file.collect())
wsr.parse_warc_records()
wsr.process_warc_records()
wsr.filter_invalid_records()
cleaned_warc_records = wsr.clean_warc_responses()
docs = cleaned_warc_records
# TODO: remove on final product
cleaned_warc_records = sc.parallelize(cleaned_warc_records.take(10))

# STAGE 2 - Entity Extraction
ee = EntityExtractor(cleaned_warc_records)
docs = ee.extract()

# to be filled

# STAGE OUTPUT - Writing as TSV
# TODO: actually write as TSV
docs_rdd = docs

print("row count: {0}".format(docs_rdd.count()))

output_rdd = docs_rdd
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv")

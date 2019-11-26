from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
sc = SparkContext()

input_file = sc.textFile("sample.warc.gz")

wsr = WARCSplitReader(sc, input_file.collect())
parsed_rdd = wsr.parse_warc_records()
print("Parsed WARC Records: {0}".format(parsed_rdd.count()))
warc_recs_rdd = wsr.process_warc_records()
print("Processed WARC Records: {0}".format(warc_recs_rdd.count()))
filtered_rdd = wsr.filter_invalid_records()
print("Filtered WARC Records: {0}".format(filtered_rdd.count()))
cleaned_warc_records = wsr.clean_warc_responses()
cleaned_warc_records.cache()
print("Cleaned WARC Records: {0}".format(cleaned_warc_records.count()))
out = cleaned_warc_records

out.repartition(1).saveAsTextFile("output/predictions.tsv")

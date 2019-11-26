from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
from EntityExtractor import EntityExtractor
sc = SparkContext()

input_file = sc.textFile("sample.warc.gz")

# STAGE 1 - INPUT READING
# -> READ warc files in a distributed manner
# -> Clean all warc records (js, style) with lxml
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

print("FINSIHED STAGE 1".format(cleaned_warc_records.count()))
# STAGE 2 - Entity Extraction
ee = EntityExtractor(cleaned_warc_records)
docs_with_entity_candidates = ee.extract()
print("Processed Docs with Entity Candidates {0}".format(docs_with_entity_candidates.count()))
out = docs_with_entity_candidates

out.repartition(1).saveAsTextFile("output/predictions.tsv")

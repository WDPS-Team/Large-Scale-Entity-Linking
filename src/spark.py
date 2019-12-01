from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
from EntityExtractor import EntityExtractor
from EntityLinker import EntityLinker
from OutputWriter import OutputWriter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--es", help="Elastic Search instance.")
parser.add_argument("--f", help="Input file.")
args = parser.parse_args()
es_path = "localhost:9200"
input_path = "sample.warc.gz"
if args.es:
    es_path = args.es
if args.f:
    input_path = args.f

print("Elastic Search Server:",es_path)
print("Input file:", input_path)

sc = SparkContext()

input_file = sc.textFile(input_path)

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
#cleaned_warc_records.repartition(1).saveAsTextFile("output/cleaned_warc_records")
fit_cleaned_warc_records = wsr.filter_unfit_records()

print("Fit WARC Records: {0}".format(fit_cleaned_warc_records.count()))
print("FINSIHED STAGE 1")

# LIMIT the records for dev:
fit_cleaned_warc_records = fit_cleaned_warc_records.sortBy(lambda row: (row["_id"]) )
fit_cleaned_warc_records = sc.parallelize(fit_cleaned_warc_records.take(20))

print("Contintue with: {0}".format(fit_cleaned_warc_records.count()))
# STAGE 2 - Entity Extraction
ee = EntityExtractor(fit_cleaned_warc_records)
docs_with_entity_candidates = ee.extract()
print("Processed Docs with Entity Candidates {0}".format(docs_with_entity_candidates.count()))
out = docs_with_entity_candidates

print("FINSIHED STAGE 2")
# STAGE 4 - Entity Linking
el = EntityLinker(docs_with_entity_candidates, es_path)
linked_entities = el.link()

print("FINISHED STAGE 4")

# # STAGE 5 - Transform and Output
ow = OutputWriter(linked_entities)
ow.transform()

output_rdd = ow.convert_to_tsv()
output_rdd.cache()
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv") #TODO: Investigate why freebase returns empty IDs (sometimes)

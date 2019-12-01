from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
from TextPreprocessor import TextPreprocessor
from EntityExtractor import EntityExtractor
from EntityLinker import EntityLinker
from OutputWriter import OutputWriter
import argparse
import ast

parser = argparse.ArgumentParser()
parser.add_argument("--es", help="Elastic Search instance.")
args = parser.parse_args()
es_path = "localhost:9200"
if args.es:
    es_path = args.es

print("Elastic Search Server:",es_path)

sc = SparkContext()

input_file = sc.textFile("step/warc_files")
filtered_rdd = input_file.map(lambda x: ast.literal_eval(x))
fittered_rdd = filtered_rdd.sortBy(lambda row: (row["id"]) )

print("STAGE 2 - Preprocessing Text")
text_prepro = TextPreprocessor(filtered_rdd)
cleaned_warc_records = text_prepro.clean_warc_responses()
cleaned_warc_records.cache()
print("\t Cleaned WARC Records: {0}".format(cleaned_warc_records.count()))

text_prepro.extract_text_from_document()
fit_cleaned_warc_records = text_prepro.filter_unfit_records()
print("\t Records fit for Extraction: {0}".format(fit_cleaned_warc_records.count()))
print("FINSIHED STAGE 2")

# LIMIT the records for dev:
fit_cleaned_warc_records = fit_cleaned_warc_records.sortBy(lambda row: (row["_id"]) )
fit_cleaned_warc_records = sc.parallelize(fit_cleaned_warc_records.take(20))

print("Contintue with: {0}".format(fit_cleaned_warc_records.count()))
# print result:
output = fit_cleaned_warc_records.take(1)
print(output)

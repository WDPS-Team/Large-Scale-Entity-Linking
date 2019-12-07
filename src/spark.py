from pyspark import SparkContext, SparkFiles, SparkConf
from WARCSplitReader import WARCSplitReader
from TextPreprocessor import TextPreprocessor
from EntityExtractor import EntityExtractor
from EntityLinker import EntityLinker
from OutputWriter import OutputWriter
from NLPPreprocessor import NLPPreprocessor
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--es", help="Elastic Search instance.")
parser.add_argument("--kb", help="Trident instance.")
parser.add_argument("--f", help="Input file.")
args = parser.parse_args()
es_path = "localhost:9200"
kb_path = "localhost:9090"
input_path = "sample.warc.gz"
if args.es:
    es_path = args.es
if args.kb:
    kb_path = args.kb
if args.f:
    input_path = args.f

print("Elastic Search Server:",es_path)
print("Trident Server:",kb_path)
print("Input file:", input_path)

conf = SparkConf().set("spark.ui.showConsoleProgress", "true")
sc = SparkContext(conf=conf)

input_file = sc.textFile(input_path)

print("STAGE 1 - Reading Input WARC")
wsr = WARCSplitReader(sc, input_file.collect())
wsr.parse_warc_records()
wsr.process_warc_records()
warc_stage_rdd = wsr.filter_invalid_records()

print("STAGE 2 - Preprocessing Text")
text_prepro = TextPreprocessor(warc_stage_rdd)
text_prepro.clean_warc_responses()
text_prepro.extract_text_from_document()
txtprepro_stage_rdd = text_prepro.filter_unfit_records()

print("STAGE 3 - NLP Preprocessing")

nlpp = NLPPreprocessor(txtprepro_stage_rdd)
nlpp.tokenization()
nlpp.lemmatize()
nlpp.stop_words()
nlpp.word_fixes()
nlpprepro_stage_rdd = nlpp.words_to_str()

# LIMIT the records for dev:
nlp_subset = nlpprepro_stage_rdd.take(17)
nlpprepro_stage_rdd = sc.parallelize(nlp_subset)

# for row in nlp_subset:
#     print(row["_id"])
#     print(row["text"])

print("STAGE 4 - Entity Extraction")
ee = EntityExtractor(nlpprepro_stage_rdd)
ee_stage_rdd = ee.extract()

print("STAGE 5 - Entity Linking")
# STAGE 4 - Entity Linking
el = EntityLinker(ee_stage_rdd, es_path)
el_stage_rdd = el.link()

print("STAGE 6 - Writing Output")
ow = OutputWriter(el_stage_rdd)
ow.transform()
ow_stage_rdd = ow.convert_to_tsv()
ow_stage_rdd.saveAsTextFile("output/predictions.tsv") #TODO: Investigate why freebase returns empty IDs (sometimes)

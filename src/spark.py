from pyspark import SparkContext, SparkFiles, SparkConf
from WARCSplitReader import WARCSplitReader
from TextPreprocessor import TextPreprocessor
from EntityExtractor import EntityExtractor
from EntityLinker import EntityLinker
from OutputWriter import OutputWriter
from NLPPreprocessor import NLPPreprocessor
from DataDisambiguator import DataDisambiguator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--es", help="Elastic Search instance.")
parser.add_argument("--kb", help="Trident instance.")
parser.add_argument("--f", help="Input file.")
parser.add_argument("--debug", help="Output some debug data.")
args = parser.parse_args()
es_path = "localhost:9200"
kb_path = "localhost:9090"
input_path = "sample.warc.gz"
debug = False
ranking_threshold = 0.5
model_root_path = "/var/scratch2/wdps1936/lib"
if args.es:
    es_path = args.es
if args.kb:
    kb_path = args.kb
if args.f:
    input_path = args.f

if args.debug == "True":
    debug = True
    model_root_path = "/data"

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

# Filter to intersting records:
if debug:
    recs=[
        "clueweb12-0000tw-00-00084"
    ]
    warc_stage_rdd = warc_stage_rdd.filter(lambda row: row["_id"] in recs)

print("STAGE 2 - Preprocessing Text")
text_prepro = TextPreprocessor(warc_stage_rdd)
text_prepro.clean_warc_responses()
text_prepro.extract_text_from_document()
txtprepro_stage_rdd = text_prepro.filter_unfit_records()
txtprepro_stage_rdd.cache()
print("STAGE 3 - NLP Preprocessing")

nlpp = NLPPreprocessor(txtprepro_stage_rdd)
nlpp.tokenization()
nlpp.lemmatize()
nlpp.stop_words()
nlpprepro_stage_rdd = nlpp.words_to_str()
nlpprepro_stage_rdd.cache()

# LIMIT the records for dev:
if debug:
    nlp_subset = nlpprepro_stage_rdd.take(5)
else:
    nlp_subset = nlpprepro_stage_rdd.take(83)
nlpprepro_stage_rdd = sc.parallelize(nlp_subset)

print("STAGE 4 - Entity Extraction")
ee = EntityExtractor(nlpprepro_stage_rdd)
ee_stage_rdd = ee.extract()
ee_stage_rdd.cache()
ee_stage_rdd = ee.join_sentences()
ee_stage_rdd.cache()

print("STAGE 5 - Entity Linking")
# STAGE 4 - Entity Linking
el = EntityLinker(ee_stage_rdd, es_path, ranking_threshold, model_root_path)
el_stage_rdd = el.get_entity_linking_candidates()
el_stage_rdd.cache()

el_stage_2_rdd = el.rank_entity_candidates()
el_stage_2_rdd.cache()

# TODO: Fetch Trident And Do The Magic Stuff
if debug:
    for row in el_stage_2_rdd.collect():
        print("---------------------")
        print(row["_id"])
        for e in row["entities_ranked_candidates"]:
            print(e["label"])
            print(e["type"])
            for c in e["ranked_candidates"]:
                print(c["similarity"])
                print(c["freebase_label"])
                print(c["freebase_id"])

print("STAGE 6 - Data Disambiguation")
dd = DataDisambiguator(el_stage_2_rdd, kb_path)
dd_stage_rdd = dd.disambiguate()

print("STAGE 7 - Writing Output")
ow = OutputWriter(dd_stage_rdd)
ow.transform()
ow_stage_rdd = ow.convert_to_tsv()
ow_stage_rdd.coalesce(1).saveAsTextFile("output/predictions.tsv") #TODO: Investigate why freebase returns empty IDs (sometimes)

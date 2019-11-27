from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader
from EntityExtractor import EntityExtractor
# from EntityLinker import EntityLinker
# from OutputWriter import OutputWriter

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

# STAGE 2 - Entity Extraction
ee = EntityExtractor(cleaned_warc_records)
docs_with_entity_candidates = ee.extract()

# STAGE 3 - Disambiguation
# to be filled

# STAGE 4 - Entity Linking
el = EntityLinker(docs_with_entity_candidates)
linked_entities = el.link()

# STAGE 5 - Transform and Output
# ow = OutputWriter(linked_entities)
# ow.transform()
# todo, sort

# output_rdd = ow.convert_to_tsv()
output_rdd = input_file
# Write
output_rdd.repartition(1).saveAsTextFile("output/predictions.tsv")

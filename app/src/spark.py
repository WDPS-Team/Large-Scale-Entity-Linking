from pyspark import SparkContext, SparkFiles
from WARCSplitReader import WARCSplitReader

sc = SparkContext()

import warcio

print(warcio)

big_list = range(10000)
rdd = sc.parallelize(big_list, 2)
odds = rdd.filter(lambda x: x % 2 != 0)
output = odds.take(5)

print("SPARK FIRST STAGE FINISHED")
print(output)

input_file = sc.textFile("sample.warc.gz")
# Convert Output:
def __splitter(input_file):
        payload = ''
        for line in input_file.collect():
            if line.strip() == "WARC/1.0":
                yield payload
                payload = line
            else:
                payload += line + "\n"

split_lines_rdd = sc.parallelize(__splitter(input_file))

wsr = WARCSplitReader(split_lines_rdd)
out = wsr.parse_warc_records()
print(out.count())

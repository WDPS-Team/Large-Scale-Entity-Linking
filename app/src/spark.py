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
wsr = WARCSplitReader(sc, input_file.collect())
print(wsr.count())

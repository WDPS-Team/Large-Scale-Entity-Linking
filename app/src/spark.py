from pyspark import SparkContext, SparkFiles
sc = SparkContext()

import warcio
print(warcio)

big_list = range(10000)
rdd = sc.parallelize(big_list, 2)
odds = rdd.filter(lambda x: x % 2 != 0)
output = odds.take(5)

print("SPARK FINISHED")
print(output)

from pyspark import SparkContext, SparkFiles
# example from https://realpython.com/pyspark-intro/
sc = SparkContext()

big_list = range(10000)
rdd = sc.parallelize(big_list, 2)
odds = rdd.filter(lambda x: x % 2 != 0)

print("it worked", odds.take(5))
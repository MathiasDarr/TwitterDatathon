#!/usr/bin/python
import findspark
findspark.init()
import pyspark as ps
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

if (__name__ == "__main__"):
    sc = spark.sparkContext
    f = sc.parallelize([1, 2, 3, 4]).collect()

    print("wordlist={}".format(f))

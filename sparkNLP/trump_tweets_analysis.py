'''
This file contains the pyspark.mllib pipeline.
'''

import findspark
findspark.init()
import pyspark as ps

from sparkNLP.utils.construct_spark_dataframe import create_tweets_dataframe, download_parquet_files

from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer


df = create_tweets_dataframe('trump')
trump_tweets_dataframe = df.filter(df['content'] != 'null')


trump_tweets_dataframe = trump_tweets_dataframe.select('content', 'date', 'location', 'username')

language_transformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
language_transformer.transform(trump_tweets_dataframe).show()


# from pyspark.ml.feature import HashingTF, Tokenizer
#
# from pyspark.mllib.clustering import KMeans, KMeansModel



(trainingData, testData) = df.randomSplit([0.7, 0.3], seed = 100)
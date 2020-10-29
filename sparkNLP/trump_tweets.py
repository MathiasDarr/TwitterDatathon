'''
This file demonstrates how to make use of the functions defined in identify_language.py & construct_spark_dataframe.py
to create a dataframe and to engineer a 'language' feature.

'''


import pyspark as ps
from pyspark.sql.types import LongType, IntegerType, ArrayType, StringType, BooleanType
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.sql.functions import udf
from sparkNLP.utils.construct_spark_dataframe import create_tweets_dataframe, download_parquet_files
from sparkNLP.utils.sparkSession import getSparkInstance
from sparkNLP.identify_language import detect_language, tokenize

#download_parquet_files('trump', [1028])

df = create_tweets_dataframe('trump')

detect_language_udf = udf(lambda content: detect_language(content), StringType())


@udf(returnType=ArrayType(StringType()))
def tokenize_udf(x):
    return tokenize(x)


tweets_dataframe = df.filter(df['content'] != 'null')
tweets_dataframe = tweets_dataframe.select('content', 'date', 'location', 'username')


tokenized_tweets_df = tweets_dataframe.select('content', 'date', 'location', 'username', tokenize_udf('content').alias('tokenized_content'))
identify_language_df = tokenized_tweets_df.select('content', 'date', 'location', 'username', 'tokenized_content', detect_language_udf('content').alias('language'))

english_virus_tweets = identify_language_df.filter(identify_language_df['language'] =='english')
english_virus_tweets = english_virus_tweets.select('content', 'date', 'location', 'username', 'tokenized_content')

italian_virus_tweets = identify_language_df.filter(identify_language_df['language'] =='italian')
italian_virus_tweets = italian_virus_tweets.select('content', 'date', 'location', 'username', 'tokenized_content')




'''
This file contains the pyspark.mllib pipeline.
'''

import findspark
findspark.init()
import pyspark as ps

from sparkNLP.utils.construct_spark_dataframe import create_tweets_dataframe, download_parquet_files
from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer
from sparkNLP.transformers.LocationTransformer import LocationParserTransformer

language_transformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
location_transformer = LocationParserTransformer(inputCol='location', outputCol='parsed_location')

df = create_tweets_dataframe('trump')
trump_tweets_dataframe = df.filter(df['content'] != 'null')

trump_tweets_dataframe = trump_tweets_dataframe.select('content', 'date', 'location', 'username')
trump_tweets_langugage_dataframe = language_transformer.transform(trump_tweets_dataframe)
location_df = location_transformer.transform(trump_tweets_langugage_dataframe)

locations_df_not_null = location_df.filter(location_df['parsed_location'] != 'null')


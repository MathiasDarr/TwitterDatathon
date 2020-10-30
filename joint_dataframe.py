"""
This file demonstrates how to join the dataset derived from the raw data & the data received from the twitter API


"""

import findspark
findspark.init()

from sparkNLP.transformers.LocationTransformer import LocationParserTransformer
from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer
from sparkNLP.transformers.SentimentAnalysisTransformer import SentimentTransformer

from pyspark.ml import Pipeline
from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet, download_parquet_files, \
    create_tweets_dataframe, concatenate_dataframes



#download_parquet_files('biden', [1028])
#download_parquet_files('trump', [1028])


# trump_tweets_dataframe = create_tweets_dataframe('trump')
#
# dataframes = [biden_tweets_dataframe, trump_tweets_dataframe]
# df = concatenate_dataframes(dataframes)


languageTransformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
locationTransformer = LocationParserTransformer(inputCol='location', outputCol='parsed_location')
sentimentTransformer = SentimentTransformer(inputCol='content')

pipeline = Pipeline(stages=[languageTransformer, locationTransformer, sentimentTransformer])

biden_tweets_dataframe = create_tweets_dataframe('biden')

pipeline_model = pipeline.fit(biden_tweets_dataframe)
biden_tweets_dataframe = pipeline_model.transform(biden_tweets_dataframe)
biden_tweets_dataframe = biden_tweets_dataframe.filter(biden_tweets_dataframe['parsed_location'] != 'null')



dataframe = create_dataframe_from_parquet('data/transformed_data')

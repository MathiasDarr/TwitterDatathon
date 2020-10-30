"""
This file demonstrates how to use the spark.ml Pipeline to perform data transformations
"""
# !/usr/bin/env python3
import findspark

findspark.init()

from sparkNLP.transformers.LocationTransformer import LocationParserTransformer
from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer
from sparkNLP.transformers.DateParserTransformer import DateParserTransformer
from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet
from sparkNLP.transformers.SentimentAnalysisTransformer import SentimentTransformer

from pyspark.ml import Pipeline
import os


def save_transformed_data_to_parquet():
    """
    This function uses the spark.ml Pipeline and custom Transformations to create new columns to the dataframe.
    Saves this dataframe to parquet. :return:
    """

    dateParserTransformer = DateParserTransformer(inputCol='date')
    languageTransformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
    locationTransformer = LocationParserTransformer(inputCol='location', outputCol='parsed_location')
    sentimentTransformer = SentimentTransformer(inputCol='content')


    pipeline = Pipeline(stages=[dateParserTransformer, languageTransformer, locationTransformer, sentimentTransformer])

    dataframe = create_dataframe_from_parquet('data/parquet')

    pipeline_model = pipeline.fit(dataframe)
    dataframe = pipeline_model.transform(dataframe)

    dataframe = dataframe.filter(dataframe['parsed_location'] != 'null')

    if not os.path.exists('data/transformed_data'):
        os.makedirs('data/transformed_data')

    dataframe.repartition(1).write.mode('overwrite').parquet('data/transformed_data')


if __name__ == '__main__':
    save_transformed_data_to_parquet()

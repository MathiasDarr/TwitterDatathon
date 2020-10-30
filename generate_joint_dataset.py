"""This script generates a concatenated dataframe & saves it to parquet The two dataframes that are being
concatenated together are the dataframe of tweets from the provided data & dataframe of tweets that have been pulled from the API and saved to parquet on s3.

"""
# !/usr/bin/env python3

import findspark
findspark.init()
from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet, download_parquet_files, \
    create_tweets_dataframe

from sparkNLP.transformation_pipeline import apply_transformation

def generate_and_save_concatenated_dataframe(download=False):
    if download:
        download_parquet_files('trump')
        download_parquet_files('biden')

    trump_tweets_dataframe = create_tweets_dataframe('trump')
    transformed_trump_tweets_dataframe = apply_transformation(trump_tweets_dataframe)

    columns_to_drop = ['_corrupt_record', 'date', 'language', 'location', 'username']
    transformed_trump_tweets_dataframe = transformed_trump_tweets_dataframe.drop(*columns_to_drop)
    transformed_trump_tweets_dataframe.cache()
    transformed_trump_tweets_dataframe.show(5)

    provided_transformed_dataframe = create_dataframe_from_parquet('data/transformed_data')
    columns_to_drop = ['date', 'id', 'location', 'retweet_count', 'verified', 'day', 'month','language']

    provided_transformed_dataframe = provided_transformed_dataframe.drop(*columns_to_drop)
    provided_transformed_dataframe.cache()
    provided_transformed_dataframe.show(5)

    # transformed_trump_tweets_dataframe

    concatendated_dataframe = transformed_trump_tweets_dataframe.union(provided_transformed_dataframe)
    concatendated_dataframe.repartition(1).write.mode('overwrite').parquet('data/concat')

if __name__ == '__main__':
    generate_and_save_concatenated_dataframe()
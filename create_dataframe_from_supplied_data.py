'''
This script will generate a dataframe from the provided dataset and save it to parquet.

That way each time I want to load the dataset I don't have to load the raw data anymore

'''
# !/usr/bin/env python3

import json
import os
import pandas as pd
from sparkNLP.utils.sparkSession import getSparkInstance
import findspark

findspark.init()

from sparkNLP.transformers.DateParserTransformer import DateParserTransformer
from sparkNLP.transformers.LocationTransformer import LocationParserTransformer
from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer
from pyspark.ml import Pipeline


def generate_data_entry(row):
    ## Generate a dictionary from a row of the pandas dataframe
    row_dictionary = {}
    row_dictionary['id'] = row.id
    row_dictionary['location'] = row.user['location']
    row_dictionary['verified'] = row.user['verified']
    row_dictionary['content'] = row.full_text
    row_dictionary['retweet_count'] = row.retweet_count
    row_dictionary['date'] = row.created_at
    return row_dictionary


def save_dataframe_to_parquet():
    '''
    Loads the raw data from & creates a Spark Dataframe which is then saved to Parquet
    '''
    data = [json.loads(line) for line in open("./data/concatenated_abridged.jsonl", 'r', encoding='utf-8')]
    df = pd.DataFrame(data)
    data = [generate_data_entry(row) for i, row in df.iterrows()]

    spark = getSparkInstance()
    dataframe = spark.createDataFrame(data)

    ## Delete the list of dictionaries & the pandas dataframe to free memory
    del data
    del df

    ### Save the dataframe to parquet  ###

    import os
    if not os.path.exists('data/parquet'):
        os.makedirs('data/parquet')

    dataframe.repartition(1).write.mode('overwrite').parquet('data/parquet')


if __name__ == '__main__':
    save_dataframe_to_parquet()

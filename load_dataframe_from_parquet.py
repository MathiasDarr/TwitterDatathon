"""This file demonstrates how to load the dataframe from parquet (the create_dataframe_from_supplied_data script must
already have been run. """


from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet

df = create_dataframe_from_parquet('data/parquet')

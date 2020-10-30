from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet
from sparkNLP.transformers.SentimentAnalysisTransformer import SentimentTransformer


dataframe = create_dataframe_from_parquet('data/transformed_data')

small_dataframe = dataframe.limit(10)

sentimentTransformer = SentimentTransformer(inputCol='content', outputCol='sentiments')

df = sentimentTransformer.transform(small_dataframe)
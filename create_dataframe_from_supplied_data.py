import json
import pandas as pd
from sparkNLP.utils.sparkSession import getSparkInstance
import findspark
findspark.init()

from sparkNLP.transformers.DateParserTransformer import DateParserTransformer
from sparkNLP.transformers.LocationTransformer import LocationParserTransformer
from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer

from pyspark.ml import Pipeline


data = [json.loads(line) for line in open("./data/data.jsonl", 'r', encoding='utf-8')]
df = pd.DataFrame(data)

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

data = [generate_data_entry(row) for i, row in df.iterrows()]

spark = getSparkInstance()
dataframe = spark.createDataFrame(data)

## Delete the list of dictionaries & the pandas dataframe
del data
del df

dateParserTransformer = DateParserTransformer(inputCol='date')
language_transformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
location_transformer = LocationParserTransformer(inputCol='location', outputCol='parsed_location')

pipeline = Pipeline(stages=[dateParserTransformer, language_transformer, location_transformer])

smaller_dataframe = dataframe.limit(5)
pipeline_model = pipeline.fit(smaller_dataframe)
smaller_dataframe = pipeline_model.transform(smaller_dataframe)

smaller_dataframe.show()

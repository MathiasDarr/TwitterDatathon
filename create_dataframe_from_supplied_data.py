import json
import pandas as pd
from sparkNLP.utils.sparkSession import getSparkInstance
import findspark
findspark.init()

from sparkNLP.transformers.DateParserTransformer import DateParserTransformer


data = [json.loads(line) for line in open("./data/data.jsonl", 'r', encoding='utf-8')]
df = pd.DataFrame(data)

def generate_data_entry(row):
    row_dictionary = {}
    row_dictionary['location'] = row.user['location']
    row_dictionary['verified'] = row.user['verified']
    row_dictionary['content'] = row.full_text
    row_dictionary['retweet_count'] = row.retweet_count
    row_dictionary['date'] = row.created_at
    return row_dictionary

data = [generate_data_entry(row) for i, row in df.iterrows()]

spark = getSparkInstance()
dataframe = spark.createDataFrame(data)

dateParserTransformer = DateParserTransformer(inputCol='date')
dataframe = dateParserTransformer.transform(dataframe)
dataframe.show(1)
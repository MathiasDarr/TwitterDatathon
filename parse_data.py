import json
import pandas as pd

data = [json.loads(line) for line in open("./data/data.jsonl", 'r', encoding='utf-8')]
df = pd.DataFrame(data)

for i, row in df.iterrows():
    id = row.id
    location = row.user['location']
    verified = row.user['verified']
    full_text = row.full_text
    retweet_count = row.retweet_count
    created_at = row.created_at

first_column = df.iloc[0]
id = first_column.id
location = first_column.user['location']
verified = first_column.user['verified']
full_text =first_column.full_text
first_column.retweet_count

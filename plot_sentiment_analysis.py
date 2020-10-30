"""
This script generates a Choropleth Map of the United States which plots the sentiment of a candidate.

"""

from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet
from sparkNLP.generate_sentiment_aggregation import generate_average_sentiment_dictionary

import plotly.graph_objects as go

import pandas as pd
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

# states_df = df.select('state', 'code')
dataframe = create_dataframe_from_parquet('data/transformed_data')
df = generate_average_sentiment_dictionary(dataframe).toPandas()
df = df[df['parsed_location'] != 'District of Columbia']
df = df.sort_values('parsed_location')
df.reset_index(drop=True, inplace=True)

index = list(range(49))

# aggregate_sentiment.set_index = index
#
# fig = go.Figure(data=go.Choropleth(
#     locations=df['code'], # Spatial coordinates
#     z = df['total exports'].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`
#     colorscale = 'Reds',
#     colorbar_title = "Millions USD",
# ))
#
# fig.update_layout(
#     title_text = '2011 US Agriculture Exports by State',
#     geo_scope='usa', # limite map scope to USA
# )
#
# fig.show()

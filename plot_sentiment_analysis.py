"""
This script generates a Choropleth Map of the United States which plots the sentiment of a candidate.

"""
# !/usr/bin/env python3

from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet
from sparkNLP.generate_sentiment_aggregation import generate_average_sentiment_dictionary

import plotly.graph_objects as go

import pandas as pd


def plot_sentiment_analysis(dataframe, candidate):
    fig = go.Figure(data=go.Choropleth(
        locations=dataframe['code'],  # Spatial coordinates
        z=dataframe['avg({}-sentiment)'.format(candidate)].astype(float),  # Data to be color-coded
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale='balance',
        colorbar_title="Sentiment",
    ))
    fig.update_layout(
        title_text='{} sentiment by state'.format(candidate.capitalize()),
        geo_scope='usa',  # limit map scope to USA
    )

    fig.show()


def generate_pandas_dataframe(dataframe):
    states_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
    states_df = states_df[['code']]
    # states_df = df.select('state', 'code')
    df = generate_average_sentiment_dictionary(dataframe).toPandas()
    df = df[df['parsed_location'] != 'District of Columbia']
    df = df.sort_values('parsed_location')
    df.reset_index(drop=True, inplace=True)

    return states_df.join(df)


if __name__ == '__main__':
    dataframe = create_dataframe_from_parquet('data/transformed_data')
    joined_dataframe = generate_pandas_dataframe(dataframe)
    plot_sentiment_analysis(joined_dataframe, 'biden')
    plot_sentiment_analysis(joined_dataframe, 'trump')

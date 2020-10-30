"""
This file contains functions for creating a dictionary where the keys are state names and the values are the average sentiment
for each candidate.

"""
from sparkNLP.utils.construct_spark_dataframe import create_dataframe_from_parquet


def generate_average_sentiment_dictionary(dataframe):
    """
    Generates a dictionary whose keys are a state name or identifying number and which has average sentiment in that state
    as a value.
    :param dataframe:
    :return:
    """
    biden_sentiment_dataframe = dataframe.groupBy('parsed_location').avg('biden-sentiment')
    trump_sentiment_dataframe = dataframe.groupBy('parsed_location').avg('trump-sentiment')
    return biden_sentiment_dataframe.join(trump_sentiment_dataframe, ['parsed_location'], how='full')


# dataframe = create_dataframe_from_parquet('data/transformed_data')
# joined_dataframe  = generate_average_sentiment_dictionary(dataframe)

# biden.crossJoin(trump).show()
#
# biden.join(trump, ['parsed_location'], how='full')
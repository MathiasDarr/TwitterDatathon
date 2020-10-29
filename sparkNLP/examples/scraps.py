# detect_language_udf = udf(lambda content: detect_language(content), StringType())
#
# @udf(returnType=ArrayType(StringType()))
# def tokenize_udf(x):
#     return tokenize(x)

# tokenized_trump_tweets_df = trump_tweets_dataframe.select('content', 'date', 'location', 'username', tokenize_udf('content').alias('tokenized_content'))
# identify_language_df = tokenized_trump_tweets_df.select('content', 'date', 'location', 'username', 'tokenized_content', detect_language_udf('content').alias('language'))
#
# english_trump_tweets = identify_language_df.filter(identify_language_df['language'] =='english')


# from pyspark.ml.feature import HashingTF, Tokenizer
#
# from pyspark.mllib.clustering import KMeans, KMeansModel
# (trainingData, testData) = df.randomSplit([0.7, 0.3], seed = 100)
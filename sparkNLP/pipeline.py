import findspark
findspark.init()
import pyspark as ps

from pyspark.sql.types import LongType, IntegerType, ArrayType, StringType, BooleanType
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.sql.functions import udf

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer


from pyspark.ml.feature import HashingTF, Tokenizer

from sparkNLP.construct_spark_dataframe import getSparkInstance, create_tweets_dataframe, download_parquet_files
from sparkNLP.identify_language import detect_language, tokenize

df = create_tweets_dataframe('trump')

detect_language_udf = udf(lambda content: detect_language(content), StringType())


@udf(returnType=ArrayType(StringType()))
def tokenize_udf(x):
    return tokenize(x)

trump_tweets_dataframe = df.filter(df['content'] != 'null')
trump_tweets_dataframe = trump_tweets_dataframe.select('content', 'date', 'location', 'username')


tokenized_trump_tweets_df = trump_tweets_dataframe.select('content', 'date', 'location', 'username', tokenize_udf('content').alias('tokenized_content'))
identify_language_df = tokenized_trump_tweets_df.select('content', 'date', 'location', 'username', 'tokenized_content', detect_language_udf('content').alias('language'))

english_trump_tweets = identify_language_df.filter(identify_language_df['language'] =='english')

(trainingData, testData) = df.randomSplit([0.7, 0.3], seed = 100)


from sparkNLP.transformers.LanguageTransformer import LanguageIdentificationTransformer

language_transformer = LanguageIdentificationTransformer(inputCol='content', outputCol='language')
language_transformer.transform(english_trump_tweets).show()





# from pyspark.ml.feature import HashingTF, Tokenizer
#
# from pyspark.mllib.clustering import KMeans, KMeansModel
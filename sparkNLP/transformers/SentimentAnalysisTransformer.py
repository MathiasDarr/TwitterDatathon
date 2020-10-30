import findspark
findspark.init()
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.pipeline import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark import keyword_only
from nltk.sentiment.vader import SentimentIntensityAnalyzer

@udf(returnType=StringType())
def sentiment_analysis_udf(location):
    '''
    This UDF is used by the transformer to feature engineer a categorical variable.

    :param location:
    :return:
    '''

    return "hello"


class SentimentTransformer(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    '''
    This transformer is used in the spark.ml pipeline to perform a transformation.
    '''

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(SentimentTransformer, self).__init__()
        self.stopwords = Param(self, "stopwords", "")
        self._setDefault(stopwords=[])
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None, stopwords=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    # Required in Spark >= 3.0
    def setInputCol(self, value):
        """
        Sets the value of :py:attr:`inputCol`.
        """
        return self._set(inputCol=value)

    # Required in Spark >= 3.0
    def setOutputCol(self, value):
        """
        Sets the value of :py:attr:`outputCol`.
        """
        return self._set(outputCol=value)

    def _transform(self, dataset):
        def f(s):
            return 'a'

        location_parser_udf('location')
        return dataset.withColumn(self.getOutputCol(), location_parser_udf(self.getInputCol()))

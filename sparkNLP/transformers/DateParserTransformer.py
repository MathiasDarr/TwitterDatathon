from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, IntegerType, StringType
from pyspark.ml.pipeline import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark import keyword_only

from sparkNLP.utils.identify_language import detect_language


@udf(returnType=StringType())
def parse_day_udf(formatted_date):
    '''
    This UDF is used by the transformer to feature engineer day & month variables.

    :param location:
    :return:
    '''
    split_date = formatted_date.split(' ')
    return split_date[2]

@udf(returnType=StringType())
def parse_month_udf(formatted_date):
    '''
    This UDF is used by the transformer to feature engineer day & month variables.

    :param location:
    :return:
    '''

    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
              'Nov': 11, 'Dec': 12}
    split_date = formatted_date.split(' ')
    return months[split_date[1]]






class DateParserTransformer(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(DateParserTransformer, self).__init__()
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
        # return dataset.withColumn('day',1)

        dataset =  dataset.withColumn('day', parse_day_udf(self.getInputCol()))
        return dataset.withColumn('month', parse_month_udf(self.getInputCol()))

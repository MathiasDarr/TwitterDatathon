from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.pipeline import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark import keyword_only
from pyspark.sql.functions import rand,when, current_date


from sparkNLP.identify_language import detect_language


# @udf(returnType=StringType())
# def identify_language_udf(x):
#     return detect_language(x)

detect_language_udf = udf(lambda content: detect_language(content), StringType())



class LanguageIdentificationTransformer(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(LanguageIdentificationTransformer, self).__init__()
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
        return dataset.withColumn('identified_language', detect_language_udf('content'))

        # return dataset.withColumn('identified_language', detect_language()

        # # t = ArrayType(StringType())
        # # out_col = self.getOutputCol()
        # # in_col = dataset[self.getInputCol()]
        # return dataset.withColumn(out_col, Column 'd')

language_transformer = LanguageIdentificationTransformer(inputCol='content', outputCol='languagee')
language_transformer.transform(english_virus_tweets).show()



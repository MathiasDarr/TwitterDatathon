import findspark
findspark.init()

from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType, DoubleType
from pyspark.ml.pipeline import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark import keyword_only

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
from nltk.parse.corenlp import CoreNLPDependencyParser


class SentimentAnalyzer:
    def __init__(self, subjects):
        '''

        :param subjects: List of subjects in which to perform sentiment analysis on e.g ['biden', 'trump']
        '''
        self.subjects = subjects
        self.dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
        self.sid = SentimentIntensityAnalyzer()

    def perform_dependency_parsing(self, text):
        '''

        :param text:
        :return:
        '''
        text = text.lower()
        parses = self.dep_parser.parse(text.split())
        return [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses][0]

    def sentiment_analysis(self, text):
        '''

        :param text:
        :return:
        '''
        dependencies = self.perform_dependency_parsing(text)
        subjects_words_dictionary = defaultdict(list)
        for dependency in dependencies:
            if dependency[1] == 'nsubj':
                subject = dependency[2][0]
                if subject == 'trump' or subject == 'biden':
                    word = dependency[0][0]
                    subjects_words_dictionary[subject].append(word)
        return subjects_words_dictionary

    def generate_sentimenet_scores(self, text):
        subjects_words_dictionary = self.sentiment_analysis(text)
        # sentiment_dictionary = {k: self.sid.polarity_scores(' '.join(v)) for k, v in subjects_words_dictionary.items() }

        sentiment_dictionary = {subject: 0.0 for subject in self.subjects}
        for k, v in subjects_words_dictionary.items():
            print(k)
            print(v)

            sentiments = self.sid.polarity_scores(' '.join(v))
            print(sentiments)
            sentiment_dictionary[k] = sentiments['compound']
        return list(v for v in sentiment_dictionary.values())


class SentimentTransformer(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    '''
    This transformer is used in the spark.ml pipeline to assign each topic found in the tweets a sentiment score
    '''

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        '''

        :param topics: list of topics on which to perform sentiment analysis e.g ['biden', 'trump']
        '''

        super(SentimentTransformer, self).__init__()
        self.stopwords = Param(self, "stopwords", "")
        self._setDefault(stopwords=[])
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

        self.sentimentAnalyzer = SentimentAnalyzer(['biden', 'trump'])

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
        sentiment_analysis_udf = udf(lambda content: self.sentimentAnalyzer.generate_sentimenet_scores(content), ArrayType(DoubleType()))
        sentiments = sentiment_analysis_udf(self.getInputCol())

        for i, subject in enumerate(self.sentimentAnalyzer.subjects):
            dataset = dataset.withColumn('{}-sentiment'.format(subject), sentiments[i])

        return dataset

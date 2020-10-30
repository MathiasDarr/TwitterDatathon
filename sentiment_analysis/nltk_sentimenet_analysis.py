from nltk.parse import CoreNLPParser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
from nltk.parse.corenlp import CoreNLPDependencyParser
# Lexical Parser
# parser = CoreNLPParser(url='http://localhost:9000')
# dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')


class SentimentAnalyzer():
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
        sentiment_dictionary = {}
        for k, v in subjects_words_dictionary.items():
            print(k)
            print(v)

            sentiments = self.sid.polarity_scores(' '.join(v))
            print(sentiments)
            sentiment_dictionary[k] = sentiments['compound']
        return sentiment_dictionary

text = 'Biden is a chump .  Trump is a genius, However Biden is a liar'

sentimentAnalyzer =  SentimentAnalyzer(['biden', 'trump'])
sentimentAnalyzer.generate_sentimenet_scores('Biden is a chump .  Trump is a genius, However Biden is a liar')

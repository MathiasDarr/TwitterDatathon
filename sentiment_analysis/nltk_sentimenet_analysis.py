"""
This file demonstrates how the SentimentAnalyzer class is used to generate a sentiment score for a selection of topics
such as bidne & trump

"""
# !/usr/bin/env python3

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
from nltk.parse.corenlp import CoreNLPDependencyParser


class SentimentAnalyzer:
    def __init__(self, subjects):
        """
        :param subjects: List of subjects in which to perform sentiment analysis on e.g ['biden', 'trump']
        """
        self.subjects = subjects
        self.dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
        self.sid = SentimentIntensityAnalyzer()

    def perform_dependency_parsing(self, text):
        """

        :param text:
        :return:
        """
        text = text.lower()
        parses = self.dep_parser.parse(text.split())
        return [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses][0]

    def sentiment_analysis(self, text):
        """

        :param text:
        :return:
        """
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
            sentiments = self.sid.polarity_scores(' '.join(v))
            sentiment_dictionary[k] = sentiments['compound']
        return sentiment_dictionary


def print_sentiments(text, sentiments):
    description = '''With this sentiment analysis method I have defined I attempt to allow for the presence of 
    multiple subjects in the input text.  A naive algorithm would only assign a single composite score.  My idea is 
    to perform dependency parsing to assign a score for each subject.  The sentiment analysis algorithm depends on 
    the presence of keywords who have been identifed as dependencies of the subject (biden or trump in example).  
    Some keywords I would hope wouuld not be neutral are as demonstrated in this example both 'genius' and 'corrupt' 
    seem to be neutral in the vader SentimentIntensityAnalyzer's mind as they appear to have impact on the sentiment 
    score. '''

    print(description)
    print()
    print(text)
    print()
    print(sentiments)


if __name__ == '__main__':
    text = 'Biden is a chump.  Trump is a genius even though he is corrupt.  Biden is a liar'
    sentimentAnalyzer = SentimentAnalyzer(['biden', 'trump'])
    sentiments = sentimentAnalyzer.generate_sentimenet_scores(text)
    print_sentiments(text, sentiments)

    # biden_sentiments = sentiments['biden']
    # trump_sentiments = sentiments['trump']
    #
    # print("The sentiment for {} is {}".format("Biden: {}".format(biden_sentiments)))
    # print("The sentiment for {} is {}".format("Biden: {}".format(trump_sentiments)))

from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from nltk.parse.stanford import StanfordParser
path_to_jars = '/data/mddarr/libraries/stanfordnlp/jars'
path_to_models_jar = '/data/mddarr/libraries/stanfordnlp/stanford-parser-4.0.0/stanford-parser-4.0.0-models.jar'
#
# from nltk.parse import stanford
# from nltk.parse.corenlp import CoreNLPParser
#
# sent = 'The quick brown fox jumps over the lazy dog.'
# next(parser.raw_parse(sent)).pretty_print()  # doctest: +NORMALIZE_WHITESPACE
#
#
# os.environ['STANFORD_PARSER'] = path_to_jars
# os.environ['STANFORD_MODELS'] = path_to_jars
#
# from nltk.parse import stanford
# parser = stanford.StanfordParser(model_path="/location/of/the/englishPCFG.ser.gz")
#
#
# # path_to_models_jar ='/data/mddarr/libraries/stanfordnlp/stanford-english-corenlp-2018-02-27-models.jar'
# # path_to_jar
# #
# # dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
# #
# # result = dependency_parser.raw_parse('I shot an elephant in my sleep')
# # dep = result.next()
# #
# # list(dep.triples())
# #
# #
# #
# # download('vader_lexicon')
# #
# # sid = SentimentIntensityAnalyzer()
# #
# # text = 'I hate Biden, but Trump is great'
# # sid.polarity_scores(text)
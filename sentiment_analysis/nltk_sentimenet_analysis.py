from nltk.parse import CoreNLPParser

# Lexical Parser
parser = CoreNLPParser(url='http://localhost:9000')

from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
parses = dep_parser.parse('Biden is a chump .  Trump is a genius'.split())

[[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses]
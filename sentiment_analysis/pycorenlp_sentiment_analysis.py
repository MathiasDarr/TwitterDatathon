from pycorenlp import StanfordCoreNLP
stanfordCoreNLP = StanfordCoreNLP('http://localhost:9000')

text = "This movie was actually neither that funny, nor super witty. The movie was meh. I liked watching that movie. If I had a choice, I would not watch that movie again."
result = stanfordCoreNLP.annotate(text,
                   properties={
                       'annotators': 'sentiment, ner, pos',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })
from nltk.parse import CoreNLPParser

coreNLPParser = CoreNLPParser(url='http://localhost:9000')

text = "This movie was actually neither that funny, nor super witty. The movie was meh. I liked watching that movie. If I had a choice, I would not watch that movie again."

result = coreNLPParser.parse(text)

'''
Test out the location parser.


'''

from sparkNLP.transformers.LocationTransformer import LocationParser

locationParser = LocationParser()
# locationParser.parse_location('WY')
# locationParser.parse_location('Springfield')

test_locations = ['WY', "jackson hole WY", ' nowhere Montana', 'Seattle']

for l in test_locations:
    locationParser.parse_location(l)

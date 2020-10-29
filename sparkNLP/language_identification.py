import findspark
findspark.init()

import re
from nltk.stem.porter import PorterStemmer
from nltk import wordpunct_tokenize
import string
from pyspark.sql.types import LongType, IntegerType, ArrayType, StringType, BooleanType
from nltk.corpus import stopwords
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.sql.functions import udf


data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
stopWords = set(stopwords.words('english'))

languages = {'danish', 'dutch', 'finnish', 'french', 'german', 'greek', 'hungarian', 'indonesian', 'italian'
             , 'norwegian', 'portuguese', 'romanian', 'russian', 'slovene', 'spanish', 'swedish', 'tajik', 'turkish' }
STOPWORDS = {}
for language in languages:
    STOPWORDS[language] = set(stopwords.words(language))

PUNCTUATION = set(string.punctuation)




def tokenize(text, language):
    """
    :param text: String
    :return: a list of tokenized words stripped of punctuation
    """
    try:
        regex = re.compile('<.+?>|[^a-zA-Z]')
        clean_txt = regex.sub(' ', text)
        tokens = clean_txt.split()
        lowercased = [t.lower() for t in tokens]
        no_punctuation = []
        for word in lowercased:
            punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
            no_punctuation.append(punct_removed)
        no_stopwords = [w for w in no_punctuation if not w in STOPWORDS[language]]

        STEMMER = PorterStemmer()
        stemmed = [STEMMER.stem(w) for w in no_stopwords]
        return [w for w in stemmed if w]
    except Exception as e:
        return ["failure"]


def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

    @param text: Text whose language want to be detected
    @type text: str

    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """
    languages_ratios = {}
    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens

    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in languages:
        # stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(STOPWORDS[language])
        languages_ratios[language] = len(common_elements)  # language "score"
    return languages_ratios


def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.
    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.
    @param text: Text whose language want to be detected
    @type text: str
    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language

@udf(returnType=ArrayType(StringType()))
def tokenize_udf(x, language):
    return tokenize(x, language)
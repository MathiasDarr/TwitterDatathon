import findspark

findspark.init()
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.pipeline import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark import keyword_only
import pandas as pd


class LocationParser:
    '''
    This class's parse_location method is made use of the by the UDF & Transformer to feature engineer a categorical
    location feature.

    '''

    def __init__(self):
        cities_df = pd.read_csv('us_cities.csv')
        cities_df.columns = [c.lower() for c in cities_df.columns]
        cities_df = cities_df.loc[cities_df.population > 50000]
        self.cities_df = cities_df[['city', 'state_name', 'lat', 'lng', 'population', 'density']]
        self.states_df = pd.read_csv('states.csv')

    def parse_location(self, location):
        state = self.parse_state(location)
        found_cities = self.parse_city(location)
        if state and found_cities:
            ###
            for city, s in found_cities:
                if s == state:
                    return state, city
        elif state and not found_cities:
            return state, self.default_location_in_state(state)

        elif not state and found_cities:
            if len(found_cities) == 1:
                pass
            else:
                ### There are cities such as Springfield that are in multiple states,
                return self.default_state_in_cities(found_cities), found_cities[1]
        else:
            return None, None

    def default_location_in_state(self, state):
        '''
        This method will assign a state a default city in the absence of a city

        :param state:
        :return:
        '''
        return 'Washington', 'Seattle'

    def default_state_in_cities(self, cities):
        '''
        This

        :param cities:
        :return:
        '''

        return 'Washington'

    def location_aliases(self):
        pass

    def parse_state(self, location):
        location = location.lower()
        location_split = location.lower().split(' ')
        for state_abrev, lat, lng, state_name in self.states_df.itertuples(index=False):
            lstate_abreviation = state_abrev.lower()
            lstate_name = state_name.lower()
            for location_word in location_split:
                if location_word == lstate_abreviation or location_word == lstate_name:
                    return state_name

    def parse_city(self, location):
        location = location.lower()
        location_split = location.lower().split(' ')
        found_cities = []
        for city, state, lat, lng, population, density in self.cities_df.itertuples(index=False):
            lcity = city.lower()

            for location_word in location_split:
                if location_word == lcity:
                    found_cities.append((city, state))
        return found_cities


locationParser = LocationParser()


class LocationParserTransformer(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    '''
    This transformer is used in the spark.ml pipeline to perform a transformation.
    '''

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(LocationParserTransformer, self).__init__()
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
        @udf(returnType=StringType())
        def location_parser_udf(location):
            '''
            This UDF is used by the transformer to feature engineer a categorical variable.
            Since it won't be used anywhere else it has been defined as an inner function
            :param location:
            :return:
            '''

            try:
                state, city = locationParser.parse_location(location)
                return state
            except:
                return None
        dataset = dataset.withColumn(self.getOutputCol(), location_parser_udf(self.getInputCol()))
        return dataset.filter(dataset['parsed_location'] != 'null')

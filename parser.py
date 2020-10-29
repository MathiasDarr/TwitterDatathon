import pandas as pd

cities_df = pd.read_csv('us_cities.csv')
cities_df.columns = [c.lower() for c in cities_df.columns]
cities_df = cities_df.loc[cities_df.population > 50000]



def parse_state(location, states_df):
    location = location.lower()
    location_split = location.lower().split(' ')
    for state_abrev, lat, lng, state_name in states_df.itertuples(index=False):
        lstate_abreviation = state_abrev.lower()
        lstate_name = state_name.lower()

        for location_word in location_split:
            if location_word == lstate_abreviation or location_word == lstate_name:
                return lstate_abreviation.upper()


def parse_city(location, cities_df):
    location = location.lower()
    location_split = location.lower().split(' ')

    found_cities = []

    for city, state, lat, lng, population, density in cities_df.itertuples(index=False):
        lcity = city.lower()

        for location_word in location_split:
            if location_word == lcity:
                found_cities.append((city, state))

    return found_cities

states_df = pd.read_csv('states.csv')
cities_df = pd.read_csv('us_cities.csv')
cities_df = cities_df[['city', 'state_name', 'lat','lng','population','density']]

cities = set()
for i in range(cities_df.count()[0] ):
    row = cities_df.iloc[i]
    cities.add(row.city)

cities = set(city[0] for city in cities_df.iterrows())

for row in cities_df.iterrows():
    print(row.city)


test_locations = ['Portland', 'Houston']
# test_locations = ['WY', "jackson hole WY", ' nowhere Montana', 'Seattle']

for l in test_locations:
    state = parse_state(l, states_df)
    city = parse_city(l, cities_df)
    print(state)
    print(city)

import pandas as pd
import numpy as np
import math
from scipy.io import loadmat, savemat

# load files for all cause mortality deaths
path = './test data/annual-number-of-deaths-by-cause.csv'
death_df = pd.read_csv(path)

# load files for population pyramid data
path = './test data/age_data.csv'
population_df = pd.read_csv(path)

# extract data for year 2017
year_list = death_df['Year']
death_index = np.where(year_list == 2017)[0]

# extract population data for year 2017
year_list = population_df['Time']
age_index = np.where(year_list == 2017)
age_index = age_index[0].reshape(-1, 21)

# store population data in a dictionary
age_data = dict()
for indices in age_index:
    country = population_df['Location'][indices[0]].lower()
    pyramid = list(population_df['PopTotal'][indices])
    age_data[country] = pyramid

# store all cause mortality death data in a dictionary
death_data = dict()
for index in death_index:
    country_death_data = death_df.values[index]
    country = country_death_data[0].lower()
    death_data[country] = [0 if math.isnan(param) else param for param in country_death_data[4:]]

country_name_map = pd.read_csv('Python Files/Neranjan/death_population_countryname_map.csv', header=None)

keywords = ['world', 'europe', 'central', 'asia', 'country', 'south']

list1, list2 = list(country_name_map[0]), list(country_name_map[1])


# check if the country name include any keywords
def check_keyword(country):
    state = False
    for keyword in keywords:
        if keyword in country:
            return not state


death_country_dict, population_country_dict = [item for item in list1], [item for item in list2]
for country1, country2 in zip(list1,list2):
    if check_keyword(country1) or check_keyword(country2):
        print(f'{country1}, {country2}')
        cmd = input('Enter command: ')
        if cmd == '':
            death_country_dict.remove(country1), population_country_dict.remove(country2)


df = pd.DataFrame({'death_country_dict': death_country_dict,
                   'population_country_dict': population_country_dict
                   })
df.to_csv('Python Files/Neranjan/death_population_countryname_map_2.csv', index=False)

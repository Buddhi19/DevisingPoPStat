import pandas as pd
import numpy as np
import math
from scipy.io import loadmat, savemat
import os

# load files for all cause mortality deaths
path = 'test data/annual-number-of-deaths-by-cause.csv'
print(os.path.abspath(path))
death_df = pd.read_csv(path)

# load files for population pyramid data
path = 'test data/age_data.csv'
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

# get the country list with all cause mortality death data
death_country_list = list(death_data.keys())

# get the country list with population pyramid data
population_country_list = list(age_data.keys())


# check if the country names are similar or one includes the other
def check_inclusion(country1, country2):
    return country1 in country2 or country2 in country1


# get the overlapping country names
exact_pairs = dict()
candidate_pairs = dict()
for death_country in death_country_list:
    candidates = [population_country for population_country in population_country_list
                  if check_inclusion(population_country, death_country)]
    candidate = [candidate for candidate in candidates if candidate == death_country]
    if len(candidate) != 0:
        try:
            exact_pairs[death_country] = candidate[0]
            population_country_list.remove(candidate[0])
        except IndexError:
            print(len(candidate))
    elif len(candidates) != 0:
        candidate_pairs[death_country] = candidates

# list with countries in both lists
primary_list = exact_pairs.keys()

for country, candidates in candidate_pairs.items():
    candidate_pairs[country] = [candidate for candidate in candidates
                                if candidate not in primary_list]

for country, candidates in candidate_pairs.items():
    candidates = dict((index, candidate) for index, candidate in enumerate(candidates))
    if len(candidates) != 0:
        print(country, candidates)
        index = input('Enter index of the candidate: ')
        if index != '':
            candidate = candidates[int(index)]
            exact_pairs[country] = candidate

death_country_dict, population_country_dict = list(exact_pairs.keys()), list(exact_pairs.values())
df = pd.DataFrame({'death_country_dict': death_country_dict,
                   'population_country_dict': population_country_dict
                   })
df.to_csv('death_population_countryname_map.csv')

import pandas as pd
import numpy as np
import math
from scipy.io import loadmat, savemat

# load files for all cause mortality deaths
path = './test data/all cause deaths.csv'
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

# get the country names mapping csv file
country_name_map = pd.read_csv('death_population_countryname_map_2.csv').values


# get the shortest name for the country
def shortest_name(name1, name2):
    if len(name1) <= len(name2):
        short_name = name1
    else:
        short_name = name2

    return short_name


prime_dict = dict()
for death_country, population_country in country_name_map:
    short_name = shortest_name(death_country, population_country)
    all_cause_mortality = death_data[death_country]
    population_pyramid = age_data[population_country]
    population_in_million = np.sum(population_pyramid)
    country_data = {'all_cause_mortality': all_cause_mortality,
                    'population_pyramid': population_pyramid,
                    'population_in_million': population_in_million}
    prime_dict[short_name] = country_data

savemat('all cause mortality.mat', prime_dict)
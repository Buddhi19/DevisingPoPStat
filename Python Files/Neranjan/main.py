from ConstructCountries import get_names_and_data
from ConstructCountries import get_countries_data
from AnalyseData import dict2array

import pandas as pd


def data_collection():

    # load files with covid data and population data
    data = get_names_and_data()

    country_list, country_name_map = data[:2]
    covid_data_frame, population_data_frame = data[2:]

    # covid_data_keys = ['total_cases', 'total_deaths', 'total_cases_per_million','total_deaths_per_million']

    covid_data_keys = ['new_cases', 'new_cases_smoothed', 'new_deaths', 'new_deaths_smoothed', 'new_cases_per_million',
                       'new_cases_smoothed_per_million', 'new_deaths_per_million', 'new_deaths_smoothed_per_million',
                       'stringency_index']

    countries_data = get_countries_data(country_list, population_data_frame, covid_data_frame,
                                        country_name_map, covid_data_keys)

    countries_data_list = dict2array(countries_data)
    print(f'Countries data of {len(countries_data_list)} countries are available.')

    # check the headers for covid data
    # print(covid_data_frame.keys())

    return countries_data


def save_countries_data(countries_data):

    path = 'D:/COVID-NER/pop pyramid/Pyramid/POPU_data/'
    country_list = countries_data.keys()
    for country in country_list:
        country_data = countries_data[country]

        # save covid related time series data
        df = pd.DataFrame(country_data['covid data'])
        file_name = path + country + '_covid_data.csv'
        df.to_csv(file_name, index=False)

        # save population pyramid data
        df = pd.DataFrame(country_data['population data'])
        file_name = path + country + '_population.csv'
        df.to_csv(file_name, index=False)


if __name__ == '__main__':
    # extract required data
    countries_data = data_collection()

    # save data for separately country-wise
    save_countries_data(countries_data)

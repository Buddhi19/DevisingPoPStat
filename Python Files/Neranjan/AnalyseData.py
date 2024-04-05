import numpy as np
import csv, time
from ConstructCountries import calculate_eta, convert_to_standard_time


def dict2array(countries_data):
    countries_data_list = list()
    start_time = time.time()
    for index, country_details in enumerate(countries_data.items()):
        country, country_data = country_details
        population_data = country_data['population data']
        covid_data = country_data['covid data']

        # convert the actual population numbers into portions
        population_data = convert2percentage(population_data)

        # calculate the time averages of covid data
        covid_data = time_averages(covid_data)
        if len(covid_data) != 0:
            countries_data_list.append([country] + population_data + covid_data)

        if (index+1) % 5 == 0 or index == len(countries_data)-1 or index == 0:
            eta_statement = \
                convert_to_standard_time(calculate_eta(index + 1, len(countries_data), start_time)
                                         )
            print(f'{len(countries_data)}/{index + 1} countries are computed.{eta_statement}')

    # write data to csv
    path_header = "./test data/"
    with open(path_header+'analyse data.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(countries_data_list)

    return countries_data_list


def convert2percentage(population_data):

    male_population = population_data['male']
    female_population = population_data['female']
    total_population = population_data['total']

    total_population = np.sum(total_population)
    male_population = male_population / total_population
    female_population = female_population / total_population

    return list(male_population) + list(female_population)


def time_averages(covid_data):

    average_data = list()
    for data_series in list(covid_data.values())[1:]:
        refined_data_series = refine_data_series(data_series)
        try:
            # time_average = refined_data_series[-1] / len(refined_data_series)
            time_average = refined_data_series[-1]
        except IndexError:
            return average_data
        average_data.append(time_average)

    return average_data


def refine_data_series(data_series):
    refined_series = list()
    for data in data_series:
        if not np.isnan(data):
            refined_series.append(data)

    return refined_series

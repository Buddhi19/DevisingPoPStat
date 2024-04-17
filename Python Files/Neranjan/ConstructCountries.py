from FileMethods import load_files, get_country_list, get_common_countries, build_list_map
from FileMethods import update_name_lists, remove_non_country_names
import time


def get_names_and_data():

    # path header for the covid and population data
    path_header = "./"
    # loading covid data files and population pyramid data files
    covid_data_df, population_df = load_files(path_header)

    # get the countries for which covid data are available
    covid_country_list = get_country_list(covid_data_df, 'location')
    # get the countries for which population pyramid data are available
    population_country_list = get_country_list(population_df, 'Location')

    # common names: generate a list with countries that appear in both files identically
    # generate a list with countries that are in covid data but population data
    common_names, different_names = get_common_countries(covid_country_list, population_country_list)

    # generate a dictionary for countries that are in both files but under different names
    # use name in owid files as key and name in population files as value
    country_name_map = build_list_map(different_names, population_country_list, path_header)

    # update the common name list and different name with the findings
    common_names, different_names = update_name_lists(country_name_map, common_names, different_names)
    common_names = sorted(common_names)

    # check if all the names in common names list of countries
    common_names = remove_non_country_names(common_names, path_header)

    return common_names, country_name_map,  covid_data_df, population_df


def get_country_population_data(country, population_data, country_name_map):

    # check if the country name exist in the country name map dictionary
    country = country_name_map.get(country, country)

    # get the starting index for the country in the 'Location' column
    country_list = list(population_data['Location'])
    country_list = [country_name.lower() for country_name in country_list]
    country_start = country_list.index(country)

    # get the starting index of the year 2020 starting from the country_start
    year = 2020
    year_start = list(population_data['Time']).index(year, country_start)
    year_end = list(population_data['Time']).index(year+1, country_start)

    # save the population pyramid data in a dictionary for the country
    country_pyramid = dict()

    country_pyramid['male'] = list(population_data['PopMale'])[year_start: year_end]
    country_pyramid['female'] = list(population_data['PopFemale'])[year_start: year_end]
    country_pyramid['total'] = list(population_data['PopTotal'])[year_start: year_end]

    return country_pyramid


def get_country_covid_data(country,owid_covid_data, headers=list()):

    # get the starting index of the country
    country_list = list(owid_covid_data['location'])
    country_list = [country_name.lower() for country_name in country_list]
    country_start = country_list.index(country)
    # reverse the country list to find the ending index of the country
    country_list.reverse()
    country_end = len(country_list) - country_list.index(country)

    time_series_data = dict()
    # save the time series for which the data is given for the country
    time_series_data['time series'] = list(owid_covid_data['date'])[country_start: country_end]

    # save the time series of the items in the 'headers' list
    for item in headers:
        time_series_data[item] = list(owid_covid_data[item])[country_start: country_end]

    return time_series_data


def get_country_data(country,population_df,covid_df,country_name_map, headers=list()):

    # extract the population data of a country in year 2020
    population_data = get_country_population_data(country, population_df, country_name_map)

    # extract the covid data of a country and the time series
    covid_data = get_country_covid_data(country, covid_df, headers=headers)

    # save the country's population and covid data
    country_data = dict()
    categories = ['population data', 'covid data']
    for category in categories:
        var = category.split()[0]+'_'+category.split()[-1]
        country_data[category] = eval(var)

    return country_data


def get_countries_data(country_list, population_df, covid_df, country_name_map, headers=list()):

    countries_data = dict()
    start_time = time.time()
    # iterate over the country list to save data
    for index, country in enumerate(country_list):
        countries_data[country] = get_country_data(country, population_df, covid_df,
                                                   country_name_map, headers=headers)

        eta_statement = convert_to_standard_time(calculate_eta(index+1, len(country_list), start_time))
        if (index + 1) % 5 == 0 or index == len(country_list)-1 or index == 0:
            print(f'{len(country_list)}/{index+1} countries are computed.{eta_statement}')

    return countries_data


def calculate_eta(epoch, epochs, start_time):

    current_time = time.time()
    spent_time = current_time - start_time
    average_time = spent_time / epoch
    eta = average_time * (epochs - epoch)
    if eta < 1 and epochs > epoch:
        eta = 1

    return int(eta)


def convert_to_standard_time(eta):

    hours = eta // 3600
    minutes = eta % 3600 // 60
    seconds = eta % 60

    time_units = [' hours ', ' minutes ', ' seconds ']
    eta_statement = ' ETA is: '

    for time_unit in time_units:
        if eval(time_unit) != 0:
            eta_statement = eta_statement + str(eval(time_unit.strip())) + time_unit

    if eta == 0:
        eta_statement = 'The process is over.\n'

    return eta_statement

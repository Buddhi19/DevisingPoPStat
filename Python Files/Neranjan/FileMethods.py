import pandas as pd
import csv


# LOAD_FILES(PATH_HEADER) will return covid data from owid site and population data from WHO site
# pandas data frames. The path header used for both files are the same, hence the files should be
# stored in the same folder


def load_files(path_header):
    # load covid data files
    url_owid_dataset = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv "
    path = url_owid_dataset
    # path = path_header + 'owid_covid_data.csv'
    covid_data_files = pd.read_csv(path)
    print('Covid data files are loaded.')

    # load population data files
    path = path_header + "test data/age_data.csv"
    print(path)
    population_data = pd.read_csv(path)
    print('Population pyramid data files are loaded.\n')

    return covid_data_files, population_data


def get_country_list(data_file, country_key=None):
    if country_key is None:
        # print the key names of file
        print(data_file.keys())

        # input the key name with country names
        country_key = input('Enter key name with country names: ')

    country_list = list(set(data_file[country_key]))

    return country_list


# GET_COMMON_COUNTRIES return two lists with identical countries and in common_names
# and countries covid data files with no reference in population files


def get_common_countries(country_lst1, country_lst2):
    # convert the country names into lower case
    country_lst1 = set([country.lower() for country in country_lst1])
    country_lst2 = set([country.lower() for country in country_lst2])

    # get the country names appear in both lists
    common_names = country_lst1.intersection(country_lst2)

    # get the country names in list 1 that are not in list 2
    different_names = country_lst1.difference(common_names)

    return sorted(list(common_names)), sorted(list(different_names))

# BUILD_LIST_MAP will construct a dictionary for the countries that appear in both lists but different names
# and a list of countries whose population pyramid data are not available


def build_list_map(different_names, compare_list, path_header, verbose=True):
    # BUILD_LIST_MAP method creates a dictionary with country names in different_names list as key
    # and corresponding name from the population data file
    # convert the country names into lower case
    different_names = [name.lower() for name in different_names]
    compare_list = [name.lower() for name in compare_list]

    # create a handle for the file with the dictionary of country name mappings
    file_name = path_header + 'country name map.csv'
    try:
        country_name_map_file = open(file_name, 'r')
        # retrieve data and store in a dictionary
        dict_reader = csv.DictReader(country_name_map_file)
        dict_reader = list(dict_reader)
        country_name_map = {country['new name']: country['old name'] for country in dict_reader}
        print('\'country name map\' file found.')
        country_name_map_file.close()
    except FileNotFoundError:
        print('Creating a file for country name map')
        country_name_map = dict()

    # create a handle for the file with the list of countries without population data
    file_name = path_header + 'no population pyramid data.csv'

    try:
        no_population_data_file = open(file_name, 'r')
        # retrieve data and store in a list
        list_reader = csv.reader(no_population_data_file)
        list_reader = list(list_reader)
        no_population_data = list()
        for country in list_reader:
            if len(country) != 0:
                no_population_data.append(country[0])
        print('\'no population pyramid data\' file found.\n')
        no_population_data_file.close()
    except FileNotFoundError:
        no_population_data = list()

    # loop thorough country names to check close names
    for query in different_names:

        # check if the country name is already in the dictionary
        new_query = country_name_map.get(query, False) is False
        if not new_query and verbose:
            # print('Key is already available for \'{}\': {}'.format(query, country_name_map[query]))
            continue
        # check if the country name is already in no population data list
        if query in no_population_data:
            continue

        query_list = list()
        for item in compare_list:
            if query in item or item in query:
                query_list.append(item)
        if len(query_list) != 0:
            print('Search results for {}'.format(query))
            print(query_list)
            query_value = input('Enter the mapping name for the query: ')
            if len(query_value) != 0:
                country_name_map[query] = query_value
            elif query not in no_population_data:
                no_population_data.append(query)
        elif query not in no_population_data:
            print('No search found for {}'.format(query))
            no_population_data.append(query)

    # write the updated dictionary
    file_name = path_header + 'country name map.csv'
    country_name_map_file = open(file_name, 'w+')
    writer = csv.writer(country_name_map_file)
    writer.writerow(['new name', 'old name'])
    for key, value in country_name_map.items():
        writer.writerow([key, value])
    # close the file
    country_name_map_file.close()

    # write the updated no population country list
    file_name = path_header + 'no population pyramid data.csv'
    no_population_data_file = open(file_name, 'w+')
    writer = csv.writer(no_population_data_file)
    for name in no_population_data:
        writer.writerow([name])
    # close the file
    no_population_data_file.close()

    return country_name_map


# UPDATE_NAME_LISTS will update the names in the common name list and different name list with the names
# found in BUILD_LIST_MAP method
def update_name_lists(country_name_map, common_names, different_names):
    for mapped_name in country_name_map.keys():
        common_names.append(mapped_name)
        different_names.remove(mapped_name)

    return common_names, different_names


# REMOVE_NON_COUNTRY_NAMES method will iterate over the list of common names
# method will write the countries removed to a separate csv file and will load previous updates
def remove_non_country_names(common_names, path_header):

    # load the csv file for the name removal
    # create a handle for the file
    file_name = path_header + 'not country names.csv'
    try:
        not_country_names_file = open(file_name, 'r')
        # retrieve data and store in a list
        list_reader = csv.reader(not_country_names_file)
        list_reader = list(list_reader)
        not_a_country = list()
        for country in list_reader:
            if len(country) != 0:
                not_a_country.append(country[0])
        print('\'not country names\' file found.')
        not_country_names_file.close()
    except FileNotFoundError:
        not_a_country = list()

    # load the csv file with country names
    # create a handle for the file
    file_name = path_header + 'country names.csv'
    try:
        is_country_names_file = open(file_name, 'r')
        # retrieve data and store in a list
        list_reader = csv.reader(is_country_names_file)
        list_reader = list(list_reader)
        is_a_country = list()
        for country in list_reader:
            if len(country) != 0:
                is_a_country.append(country[0])
        print('\'country names\' file found.\n')
        is_country_names_file.close()
    except FileNotFoundError:
        is_a_country = list()

    iterate_list = [name for name in common_names]

    # iterate over the list of countries in common names list
    for index, name in enumerate(iterate_list):
        # check if the country is already available:: remove if true
        if name in not_a_country:
            # print(f'{name} found in not a country list')
            common_names.remove(name)
            continue
        # check if the country is already available:: move to the next country
        elif name in is_a_country:
            # print(f'{name} found in country list')
            continue

        decision = input(f'Is {len(iterate_list)}/{index+1}:\'{name}\' a country? Press \'Enter\' or another key: ')

        if len(decision) != 0:
            not_a_country.append(name)
            common_names.remove(name)

    # write the updated not country list
    file_name = path_header + 'not country names.csv'
    not_country_names_file = open(file_name, 'w+')
    writer = csv.writer(not_country_names_file)
    for name in not_a_country:
        writer.writerow([name])
    # close the file
    not_country_names_file.close()

    # write the updated country list
    file_name = path_header + 'country names.csv'
    is_country_names_file = open(file_name, 'w+')
    writer = csv.writer(is_country_names_file)
    for name in common_names:
        writer.writerow([name])
    # close the file
    is_country_names_file.close()

    return common_names

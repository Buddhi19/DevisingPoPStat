import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def not_important():

    '''blacklist_countries = list()
    while True:
        country = input('Enter blacklist country: ')
        if len(country) == 0:
            break
        blacklist_countries.append(country)

    path = 'C:/Users/pc-user/Desktop/population study/'
    df = pd.DataFrame(blacklist_countries)
    file_name = path + 'blacklist_countries.csv'
    df.to_csv(file_name, index=False)'''

    path = 'population_study/first_wave_locations_'

    first_wave_locations = list()
    for file_index in range(1, 9):
        file_name = path + str(file_index) + '.csv'
        df = pd.read_csv(file_name).values
        for mini_list in df:
            first_wave_locations.append([mini_list[0], mini_list[1]])

    path = 'population_study/first_wave_locations'
    df = pd.DataFrame(first_wave_locations)
    file_name = path + '.csv'
    df.to_csv(file_name, index=False)


def smooth_time_series_data(time_series_data, interval=14):
    smooth_signal_time_stamps = list()
    smooth_signal = list()

    for index in range(len(time_series_data) - interval + 1):
        signal_window = time_series_data[index: index + interval]
        smooth_signal.append(np.average(signal_window))

    return smooth_signal


def resample_indices(signal, samples):
    indices = np.linspace(0, len(signal)-1, samples)
    indices = [int(index) for index in indices]

    return indices


def align_wave(signal1, signal2):

    signal1 = [0 if pd.isna(item) else item for item in signal1]
    signal2 = [0 if pd.isna(item) else item for item in signal2]

    if len(signal1) < len(signal2):
        indices = resample_indices(signal2, len(signal1))
        resample_signal = [signal2[index] for index in indices]
        ref_signal = signal1
    elif len(signal1) > len(signal2):
        indices = resample_indices(signal1, len(signal2))
        resample_signal = [signal1[index] for index in indices]
        ref_signal = signal2
    else:
        resample_signal, ref_signal = signal1, signal2

    return np.asarray(resample_signal), np.asarray(ref_signal)


def get_country_list():
    path = 'population_study'
    df = pd.read_csv(path + '/first_wave_locations.csv')
    countries_data = df.values
    path += '/my_files/'

    country_count = len(countries_data)
    corr_mat, pop_dist_mat = np.zeros((country_count, country_count)), np.zeros((country_count, country_count))

    for ref_index, ref_country_data in enumerate(countries_data):

        country_name = ref_country_data[0]
        file_name = path + country_name
        covid_data = pd.read_csv(file_name+'_covid.csv')['new_cases_smoothed_per_million']
        population_data = pd.read_csv(file_name+'_population.csv')['total']

        time_span = 28  # days
        smooth_signal = smooth_time_series_data(covid_data, interval=time_span)
        wave_location = ref_country_data[1]
        ref_wave = smooth_signal[:wave_location+1]
        ref_pyramid = population_data / np.sum(population_data)

        for target_index in range(ref_index+1, len(countries_data)):
            country_name = countries_data[target_index][0]
            file_name = path + country_name
            covid_data = pd.read_csv(file_name+'_covid.csv')['new_cases_smoothed_per_million']
            population_data = pd.read_csv(file_name+'_population.csv')['total']

            time_span = 28  # days
            smooth_signal = smooth_time_series_data(covid_data, interval=time_span)
            wave_location = ref_country_data[1]
            target_wave = smooth_signal[:wave_location + 1]
            target_pyramid = population_data / np.sum(population_data)

            resample_signal, ref_signal = align_wave(target_wave, ref_wave)

            corr_mat[ref_index, target_index] = np.corrcoef(resample_signal, ref_signal)[0, 1]
            pop_dist_mat[ref_index, target_index] = np.linalg.norm(ref_pyramid-target_pyramid)
            print(ref_index, target_index)
    return corr_mat, pop_dist_mat


dependent_var, independent_var = get_country_list()
dependent_matrix = dependent_var + dependent_var.T
independent_matrix = independent_var + independent_var.T

max_index, max_corr = 0, 0
for index in range(dependent_matrix.shape[0]):
    dep_vector, ind_vector = dependent_matrix[index], independent_matrix[index]
    dep_vector, ind_vector = np.delete(dep_vector, index), np.delete(ind_vector, index)

    corr = np.corrcoef(dep_vector, ind_vector)[0, 1]
    if abs(corr) > max_corr:
        max_index = index
        max_corr = abs(corr)

ref_dep_vector, ref_ind_vector = dependent_matrix[max_index], independent_matrix[max_index]
ref_dep_vector = np.delete(ref_dep_vector, max_index)
ref_ind_vector = np.delete(ref_ind_vector, max_index)

plt.scatter(ref_ind_vector, ref_dep_vector)

file_name = 'population_study/first_wave_locations.csv'
ref_country = pd.read_csv(file_name)['0'][max_index]

plt.title(f'Reference country {ref_country} with a corr coef {np.corrcoef(ref_ind_vector, ref_dep_vector)}')
plt.show()

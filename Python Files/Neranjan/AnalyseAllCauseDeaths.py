from scipy.io import loadmat
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import re

# load mat file with population data and all cause mortality data
prime_dict = loadmat('all cause mortality.mat')


# calculate the distance between two population pyramids
def pyramid_distance(pyramid1, pyramid2):
    diff = pyramid1 - pyramid2
    return np.linalg.norm(diff)


# calculate the median age of the country
def calculate_median_age(country, total):
    pyramid = np.copy(country) / total
    cum_pop = 0
    for bin, pop_mass in enumerate(pyramid):
        cum_pop += pop_mass
        if cum_pop >= 0.5:
            lower_limit = bin * 5
            median_age = lower_limit + 5 * (0.5 + pop_mass - cum_pop) / pop_mass
            break
    return median_age

# create the dictionary for csv file
csv_dict = dict()


# font sizes for the plots
label_font, ax_font, legend_font = 15, 12, 12


# clean the mat file dictionary
country_data = dict()
country_list = list(prime_dict.keys())[4:]

csv_dict['country'] = country_list

for country in country_list:
    deaths, age_data, population = prime_dict[country][0][0]
    deaths, age_data, population = deaths[0], age_data[0], population[0][0]
    country_data[country] = {'deaths': deaths,
                             'age_data': age_data,
                             'population': population}

# set the country with the lowest median age as the reference country
country_median_age = dict()
for country in country_data.keys():
    data = country_data[country]
    country_median_age[country] = calculate_median_age(data['age_data'], data['population'])

reference_country = np.argmin(list(country_median_age.values()))
reference_country = list(country_median_age.keys())[reference_country]


# all cause mortality correlation with population pyramid
all_cause_deaths, distance_from_reference = list(), list()
ref_pyramid = country_data[reference_country]['age_data']/country_data[reference_country]['population']

for country, data in country_data.items():
    deaths, pyramid, population = data['deaths'], data['age_data'], data['population']
    total_deaths_per_million = np.sum(deaths) / population
    all_cause_deaths.append(total_deaths_per_million)

    distance = pyramid_distance(pyramid/population, ref_pyramid)
    distance_from_reference.append(distance)

csv_dict['all cause'] = all_cause_deaths
correlation_coefficient = np.corrcoef(distance_from_reference, all_cause_deaths)[0,1]

plt.scatter(distance_from_reference, all_cause_deaths)
reference_country = reference_country[0].upper() + reference_country[1:]
plt.xlabel(f'Disparity with {reference_country} demography distribution', fontsize=label_font)
plt.ylabel(f'Deaths per million', fontsize=label_font)




# plt.title(f'Variation of all cause mortality with population pyramid distance from {reference_country}\n'
#           f'(corr. coef = {correlation_coefficient})', fontsize=10)
description = ['all cause']
corr_coef = [correlation_coefficient]
# plt.savefig('C:/Users/pc-user/Desktop/population study/all cause deaths/paper/all_cause.png', format='png', bbox_inches='tight', transparent=True)

# specific cause mortality correlation with population pyramid
# load files for all cause mortality deaths
path = 'C:/Users/pc-user/Desktop/population study/all cause deaths/all cause deaths.csv'
death_df = pd.read_csv(path)
death_causes = list(death_df.keys()[4:])

per_figure_subplots = 4

for index, cause in enumerate(death_causes):
    if cause.startswith('Death'):
        cause = cause.split(' - ')[1]
        death_causes[index] = cause

figure_count = 0
for index, cause in enumerate(death_causes):
    cause_country_list, cause_death_list, cause_age_list, cause_median_age_list = list(), list(), list(), list()

    test_country_list = list()
    for country in country_list:
        try:
            cause_deaths = country_data[country]['deaths'][index]
            test_country_list.append(country)
        except IndexError:
            print('Error is still there')
        if cause_deaths != 0:
            country_population = country_data[country]['population']

            cause_country_list.append(country)
            cause_death_list.append(cause_deaths/country_population)
            cause_age_list.append(country_data[country]['age_data']/country_population)
            cause_median_age_list.append(country_median_age[country])

    # print(len(test_country_list), len(cause_country_list), cause)

    if len(cause_country_list) != 0:
        cause_reference_country = np.argmin(cause_median_age_list)
        cause_reference_pyramid = cause_age_list[cause_reference_country]
        cause_reference_country = cause_country_list[cause_reference_country]

        cause_distance_from_reference = list()
        for country_pyramid in cause_age_list:
            distance = pyramid_distance(cause_reference_pyramid, country_pyramid)
            cause_distance_from_reference.append(distance)

        correlation_coefficient = np.corrcoef(cause_distance_from_reference, np.log(cause_death_list))[0, 1]

#        if figure_count % per_figure_subplots == 0:
#            fig, axes = plt.subplots(nrows=2, ncols=2)
#            fig.tight_layout()  # Or equivalently,  "plt.tight_layout()"

#        row = (figure_count % per_figure_subplots) % 2
#        col = (figure_count % per_figure_subplots) // 2

#        axes[row][col].scatter(cause_distance_from_reference, np.log(cause_death_list))
        #plt.xlabel(f'Distance from {reference_country}', fontsize=8)
        #plt.ylabel(f'Specific cause mortality per million', fontsize=8)
#        axes[row][col].set_title(f'Variation of Specific cause mortality with population pyramid distance from '
#                                 f'{reference_country}\n for {cause}(corr. coef = {correlation_coefficient})',
#                                 size=8)

        csv_dict['_'.join(re.split(' |/', cause)).lower()] = cause_death_list
        # plot individual scatter plots
        plt.figure()
        plt.scatter(cause_distance_from_reference, cause_death_list)
        reference_country = reference_country[0].upper() + reference_country[1:]
        plt.xlabel(f'Disparity with {reference_country} demography distribution', fontsize=label_font)
        plt.ylabel(f'Deaths per million', fontsize=label_font)
        fig_path = 'C:/Users/pc-user/Desktop/population study/all cause deaths/paper/' + \
                   '_'.join(re.split(' |/', cause)).lower() + '.png'
        plt.title(cause)
        print(cause, fig_path)
        # plt.savefig(fig_path, format='png', bbox_inches='tight', transparent=True)

        description.append([cause, len(test_country_list)])
        corr_coef.append(correlation_coefficient)
        figure_count += 1

'''
df = pd.DataFrame({'description': description,
                   'correlation coefficient': corr_coef,
                   'abs': np.abs(corr_coef)})
df.to_csv('correlation results.csv', index=False)
'''
plt.show()
# print(description)

# df = pd.DataFrame(csv_dict)
# df.to_csv('C:/Users/pc-user/Desktop/population study/all cause deaths/paper/specific cause deaths.csv')
# for key in csv_dict.keys():
#     print(len(csv_dict[key]))

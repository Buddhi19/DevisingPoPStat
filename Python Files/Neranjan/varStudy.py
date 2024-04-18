import pandas as pd
import numpy as np
from scipy.io import savemat
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

path = 'population_study'
df = pd.read_csv(path + '/first_wave_locations.csv')
countries_data = df.values
path += '/my_files/'

country_count = len(countries_data)
corr_mat, pop_dist_mat = np.zeros((country_count, country_count)), np.zeros((country_count, 1))
stat_mat = np.zeros((country_count, 3))

ref_pyramid = pd.read_csv(path+'niger_population.csv')['total']
ref_pyramid = ref_pyramid / np.sum(ref_pyramid)

for ref_index, ref_country_data in enumerate(countries_data):

    country_name = ref_country_data[0]
    file_name = path + country_name
    covid_data = pd.read_csv(file_name+'_covid_data.csv')['new_cases_smoothed_per_million']
    population_data = pd.read_csv(file_name+'_population.csv')['total']
    target_pyramid = population_data / np.sum(population_data)

    wave_location = ref_country_data[1]
    stat_mat[ref_index, 0] = wave_location
    stat_mat[ref_index, 1] = np.max(covid_data[:wave_location+1])
    stat_mat[ref_index, 2] = np.sum(covid_data[:wave_location+1])

    pop_dist_mat[ref_index] = np.linalg.norm(ref_pyramid-target_pyramid)

mat_scaler = StandardScaler()
scaled_stat_mat = mat_scaler.fit_transform(stat_mat)

train_data = np.concatenate((scaled_stat_mat, pop_dist_mat), axis=1)

print(stat_mat.shape, pop_dist_mat.shape, train_data.shape)
m_dict = {'train data': train_data}
savemat('train_data.mat', m_dict)

'''# Apply PCA to the scaled dataset
pca = PCA(n_components=2)
reduced_stat_mat = pca.fit_transform(scaled_stat_mat)
print(reduced_stat_mat)'''


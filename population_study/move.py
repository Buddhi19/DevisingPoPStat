# copy files named as covid_data.csv from POPU_data to my_files

import os
import shutil

path = 'POPU_data/'
file_names = os.listdir(path)
for file_name in file_names:
    shutil.copy(path + file_name, 'population_study/my_files/' + file_name)


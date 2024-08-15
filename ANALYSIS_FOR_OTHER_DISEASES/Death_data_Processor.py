import os
import pandas as pd
import numpy as np
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name

DEATH_DATA_1 = os.path.join(main_dir, 'DATA/DEATH_DATA/IHME-GBD_2021_DATA-1.csv')
DEATH_DATA_2 = os.path.join(main_dir, 'DATA/DEATH_DATA/IHME-GBD_2021_DATA-2.csv')
DEATH_DATA_3 = os.path.join(main_dir, 'DATA/DEATH_DATA/IHME-GBD_2021_DATA-3.csv')
DEATH_DATA_4 = os.path.join(main_dir, 'DATA/DEATH_DATA/IHME-GBD_2021_DATA-4.csv')
DEATH_DATA_5 = os.path.join(main_dir, 'DATA/DEATH_DATA/IHME-GBD_2021_DATA-5.csv')

SAVE_PATH = os.path.join(main_dir, 'DATA/DEATH_DATA/DEATH_DATA.csv')


def DEATH_DATA_PROCESSOR(year):
    death_data_1 = pd.read_csv(DEATH_DATA_1, low_memory = False)
    death_data_2 = pd.read_csv(DEATH_DATA_2, low_memory = False)
    death_data_3 = pd.read_csv(DEATH_DATA_3, low_memory = False)
    death_data_4 = pd.read_csv(DEATH_DATA_4, low_memory = False)
    death_data_5 = pd.read_csv(DEATH_DATA_5, low_memory = False)
    death_data = pd.concat([death_data_1, death_data_2, death_data_3, death_data_4, death_data_5])
    death_data = death_data.dropna()
    # drop columns
    death_data = death_data.drop(columns=['upper', 'lower', 'measure_id',
                                             'measure_name', 'metric_id', 'location_id','sex_id', 'age_id'])
    death_data = death_data.drop_duplicates()
    death_data = death_data[death_data['year'] == year]
    #save
    death_data.to_csv(SAVE_PATH, index=False)

if __name__ == '__main__':
    DEATH_DATA_PROCESSOR(2021)
    print('Death data processed successfully')

    
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
SAVE_PATH_FOR_SPAN = os.path.join(main_dir, 'DATA/DEATH_DATA/DEATH_DATA_FOR_SPAN.csv')

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

def DEATH_DATA_PROCESSOR_FOR_SPAN(start_year,end_year):
    death_data_1 = pd.read_csv(DEATH_DATA_1, low_memory = False)
    death_data_2 = pd.read_csv(DEATH_DATA_2, low_memory = False)
    death_data_3 = pd.read_csv(DEATH_DATA_3, low_memory = False)
    death_data_4 = pd.read_csv(DEATH_DATA_4, low_memory = False)
    death_data_5 = pd.read_csv(DEATH_DATA_5, low_memory = False)
    death_data = pd.concat(
        [death_data_1,death_data_2,death_data_3,death_data_3,death_data_4,death_data_5]
    )
    death_data = death_data.drop(columns=['upper', 'lower', 'measure_id',
                                             'measure_name', 'metric_id', 'location_id','sex_id', 'age_id'])
    death_data = death_data.drop_duplicates()
    death_data = death_data[(death_data['year'] >= start_year) & (death_data['year'] <= end_year)]
    death_data = death_data[death_data["metric_name"] == "Rate"]
    DATAFRAME_WITH_SUM_OF_DEATH_COUNT = {
        column : [] for column in death_data.columns
    }
    for disease in death_data["cause_id"].unique():
        death_data_for_disease = death_data[death_data["cause_id"] == disease]
        for country in death_data_for_disease["location_name"].unique():
            death_data_for_country = death_data_for_disease[death_data_for_disease["location_name"] == country]
            total_death_count = death_data_for_country["val"].sum()
            for column in death_data.columns:
                if column == "val":
                    DATAFRAME_WITH_SUM_OF_DEATH_COUNT[column].append(total_death_count)
                elif column == "year":
                    DATAFRAME_WITH_SUM_OF_DEATH_COUNT[column].append(f"{start_year}-{end_year}")
                else:
                    DATAFRAME_WITH_SUM_OF_DEATH_COUNT[column].append(death_data_for_country[column].values[0])

    DATAFRAME_WITH_SUM_OF_DEATH_COUNT = pd.DataFrame(DATAFRAME_WITH_SUM_OF_DEATH_COUNT)
    DATAFRAME_WITH_SUM_OF_DEATH_COUNT.to_csv(SAVE_PATH_FOR_SPAN, index=False)


if __name__ == '__main__':
    DEATH_DATA_PROCESSOR_FOR_SPAN(2017,2021)

    
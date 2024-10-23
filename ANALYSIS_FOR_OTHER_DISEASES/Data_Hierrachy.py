import sys
import os

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

import pandas as pd

from ANALYSIS_FOR_OTHER_DISEASES.eval import DATAFRAME

DATA_HIERARCHY_PATH = os.path.join(main_dir, 'DATA', 'death_data','Cause_Mapping.csv')
DATA_HIERARCHY = pd.read_csv(DATA_HIERARCHY_PATH, low_memory=False)

DEATH_DATA_RESULTS_PATH = os.path.join(main_dir, 'RESULTS', 'CORRELATION_DATA_FOR_OTHER_DISEASES',
                                       'Correlation_Coefficient_custom.csv')

DEATH_DATA_RESULTS = pd.read_csv(DEATH_DATA_RESULTS_PATH, low_memory=False)

def get_all_level_Diseases(level:int):
    list_all_diseases = DATA_HIERARCHY[DATA_HIERARCHY['Level'] == level]['Cause Name'].values
    return list_all_diseases, len(list_all_diseases)

def filter_diseases_by_level(level:int):
    list_all_diseases = get_all_level_Diseases(level)[0]
    filtered_data = DEATH_DATA_RESULTS[DEATH_DATA_RESULTS['Cause of Death'].isin(list_all_diseases)]

    DATAFRAME = {
        'Cause of Death': [],
        'PoPStat': [],
        'PoPStat R value' : [],
        'Reference': [],
        'HDI': [],
        'SDI': [],
        'Median Age': [],
        'GDP per capita': [],
        'Population Density': [],
        'Gini coefficient': [],
        'UHCI': [],
        'Life expectancy': []
    }

    for disease in filtered_data['Cause of Death'].unique():
        DATAFRAME['Cause of Death'].append(disease)
        data_per_disease = filtered_data[filtered_data['Cause of Death'] == disease]
        PoPStat_data = data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['r squared value'].values[0]
        PoPStat_R_val = data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['R value'].values[0]
        DATAFRAME['PoPStat'].append(PoPStat_data)
        DATAFRAME['Reference'].append(
            data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['reference_country'].values[0]
        )
        DATAFRAME['PoPStat R value'].append(PoPStat_R_val)
        for parameter in [
            'HDI', 'SDI', 'Median Age', 'GDP per capita', 'Population Density', 'Gini coefficient', 'UHCI', 'Life expectancy'
        ]:
            try:
                DATAFRAME[parameter].append(
                    data_per_disease[data_per_disease['Parameter'] == parameter]['r squared value'].values[0]
                )
            except:
                DATAFRAME[parameter].append(None)

    DATAFRAME = pd.DataFrame(DATAFRAME)
    DATAFRAME = DATAFRAME.sort_values(by='PoPStat', ascending=False)
    DATAFRAME.to_csv(os.path.join(main_dir, 'RESULTS', 'POPSTAT_OTHER_DISEASES',
                                      f'Correlation_for_level{level}_diseases.csv'), index=False)

if __name__ == '__main__':
    for i in range(1, 5):
        filter_diseases_by_level(i)
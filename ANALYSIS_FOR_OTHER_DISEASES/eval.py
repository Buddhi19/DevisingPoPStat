import os
import sys
import pandas as pd

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

DATA_PATH = os.path.join(main_dir,'RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/Correlation_Coefficient_custom.csv')
GLOBAL_DEATH_DATA_PATH = os.path.join(main_dir, 'DATA/death_data/Global_Deaths.csv')

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

PARAMETERS = [
    "PoPStat", "HDI", "SDI", "Median Age", "GDP per capita", "Population density", "Gini coefficient", "UHCI", "Life expectancy"
]

def EVAL_FOR_BEST():
    data = pd.read_csv(DATA_PATH)
    count = 0
    for disease in data['Disease'].unique():
        data_per_disease = data[data['Disease'] == disease]

        r_squared_values = [
            data_per_disease[f'{parameter} r squared'].values[0] for parameter in PARAMETERS
        ]
        if max(r_squared_values) == r_squared_values[0]:
            count+=1

    print(f"Total of {count} diseases are ranked first with POPSTAT")



if __name__ == '__main__':
    EVAL_FOR_BEST()
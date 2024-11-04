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

def EVAL_FOR_BEST(num: int):
    data = pd.read_csv(DATA_PATH)
    count = 0
    for disease in data['Cause of Death'].unique():
        data_per_disease = data[data['Cause of Death'] == disease]
        Dict = {}
        for parameter in [
            'HDI', 'SDI', 'Median Age', 'GDP per capita', 'Population Density', 'Gini coefficient', 'UHCI', 'Life expectancy', f'POPSTAT_{disease}'
        ]:
            try:
                Dict[parameter] = data_per_disease[data_per_disease['Parameter'] == parameter]['r squared value'].values[0]
            except:
                Dict[parameter] = 0

        sorted_dict = dict(sorted(Dict.items(), key=lambda item: item[1], reverse=True))
        best = list(sorted_dict.keys())[num-1]

        if best == f'POPSTAT_{disease}':
            DATAFRAME['Cause of Death'].append(disease)
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
                DATAFRAME[parameter].append(
                    data_per_disease[data_per_disease['Parameter'] == parameter]['r squared value'].values[0]
                )
            count += 1
        
    print(f"Total of {count} diseases are ranked {num} with POPSTAT")

def convert_to_DATAFRAME(path:str):
    data = pd.read_csv(path)
    DATAFRAME_WITH_DEATH_COUNT = {
        'Cause of Death': [],
        'PoPStat': [],
        'PoPStat R value' : [],
        'Reference': [],
        'Death Count': [],
        'HDI': [],
        'SDI': [],
        'Median Age': [],
        'GDP per capita': [],
        'Population Density': [],
        'Gini coefficient': [],
        'UHCI': [],
        'Life expectancy': []
    }
    global_death_data = pd.read_csv(GLOBAL_DEATH_DATA_PATH)
    for disease in data['Cause of Death'].unique():
        data_per_disease = data[data['Cause of Death'] == disease]
        PoPStat_data = data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['r squared value']
        if PoPStat_data.empty:
            continue
        PoPStat_data = PoPStat_data.values[0]
        DATAFRAME_WITH_DEATH_COUNT['Cause of Death'].append(disease)
        global_death_per_disease = global_death_data[global_death_data['cause_name'] == disease]
        if global_death_per_disease.empty:
            DATAFRAME_WITH_DEATH_COUNT['Death Count'].append(0)
        else:
            global_death_count = global_death_per_disease[
                global_death_per_disease['metric_name'] == 'Rate'
            ]['val'].values[0]
            DATAFRAME_WITH_DEATH_COUNT['Death Count'].append(global_death_count)
        
        PoPStat_R_val = data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['R value'].values[0]
        DATAFRAME_WITH_DEATH_COUNT['PoPStat'].append(PoPStat_data)
        DATAFRAME_WITH_DEATH_COUNT['Reference'].append(
            data_per_disease[data_per_disease['Parameter'] == f'POPSTAT_{disease}']['reference_country'].values[0]
        )
        DATAFRAME_WITH_DEATH_COUNT['PoPStat R value'].append(PoPStat_R_val)
        for parameter in [
            'HDI', 'SDI', 'Median Age', 'GDP per capita', 'Population Density', 'Gini coefficient', 'UHCI', 'Life expectancy'
        ]:
            try:
                DATAFRAME_WITH_DEATH_COUNT[parameter].append(
                    data_per_disease[data_per_disease['Parameter'] == parameter]['r squared value'].values[0]
                )
            except:
                DATAFRAME_WITH_DEATH_COUNT[parameter].append(0)

    DATAFRAME_WITH_DEATH_COUNT = pd.DataFrame(DATAFRAME_WITH_DEATH_COUNT)
    DATAFRAME_WITH_DEATH_COUNT = DATAFRAME_WITH_DEATH_COUNT.sort_values(by='Death Count', ascending=False)
    pd.DataFrame(DATAFRAME_WITH_DEATH_COUNT).to_csv(f'RESULTS/POPSTAT_OTHER_DISEASES/COUNTING/POPSTAT_ALL_with_death_count.csv', index=False)


def convert_communicable():
    # data_path = os.path.join(main_dir, 'RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/Correlation_Coefficient_communicable.csv')
    data_path = DATA_PATH
    convert_to_DATAFRAME(data_path)
    return


if __name__ == '__main__':
    convert_communicable()    
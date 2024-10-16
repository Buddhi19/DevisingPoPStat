import os
import sys
import pandas as pd

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

DATA_PATH = os.path.join(main_dir,'RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/Correlation_Coefficient_custom.csv')

DATAFRAME = {
        'Cause of Death': [],
        'PoPStat': [],
        'HDI': [],
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
            'HDI', 'Median Age', 'GDP per capita', 'Population Density', 'Gini coefficient', 'UHCI', 'Life expectancy', f'POPSTAT_{disease}'
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
            DATAFRAME['PoPStat'].append(PoPStat_data)

            for parameter in [
                'HDI', 'Median Age', 'GDP per capita', 'Population Density', 'Gini coefficient', 'UHCI', 'Life expectancy'
            ]:
                DATAFRAME[parameter].append(
                    data_per_disease[data_per_disease['Parameter'] == parameter]['r squared value'].values[0]
                )
            count += 1
        
    print(f"Total of {count} diseases are ranked {num} with POPSTAT")
    for key in DATAFRAME:
        DATAFRAME[key].append("")


if __name__ == '__main__':
    EVAL_FOR_BEST(1)
    EVAL_FOR_BEST(2)
    EVAL_FOR_BEST(3)
    pd.DataFrame(DATAFRAME).to_csv('RESULTS/POPSTAT_OTHER_DISEASES/Best_Results.csv', index=False)
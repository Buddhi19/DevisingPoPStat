import os
import sys
import pandas as pd

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

DATA_PATH = os.path.join(main_dir, 'RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/Correlation_Coefficient_japan_KLD.csv')

def EVAL():
    data = pd.read_csv(DATA_PATH)
    for disease in data['Cause of Death'].unique():
        data_per_disease = data[data['Cause of Death'] == disease]
        # if max of r squared value of parameters is popstat then print it
        if data_per_disease['r squared value'].max() == data_per_disease[data_per_disease['Parameter'] == 'POPSTAT_COVID19']['r squared value'].values[0]:
            print(f"{disease} is best fitted with POPSTAT with R squared value of {data_per_disease['r squared value'].max()}")


if __name__ == '__main__':
    EVAL()
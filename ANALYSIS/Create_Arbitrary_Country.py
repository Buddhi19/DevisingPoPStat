import os
import sys
import pandas as pd
import numpy as np

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

RESULTS_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_COUNTRY_DATA')

from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Plot_Pop_Stat import PLOT_POP_STAT

def CREATE_ARBITRARY_COUNTRY():
    pop_stat_calculator = POP_STAT_CALCULATION()
    pop_stat_calculator.remove_nan_values()
    AGE_GROUPS = [
        "0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90-94","95-99","100+"
    ]
    country_name = "Arbitrary"
    pop_array= [1 for i in range(len(AGE_GROUPS))]
    pop_array_normalized = np.array(pop_array)/np.array(pop_array).sum()
    pop_stat_calculator.population_data[country_name] = pop_array_normalized
    data = pop_stat_calculator.POPSTAT_COVID19(country_name)
    data = pd.DataFrame(data.items(), columns = ['Country', 'POPSTAT_COVID19'])
    data.to_csv(os.path.join(RESULTS_DIR, f'{country_name}_POPSTAT_COVID19.csv'), index = False)

def PLOT_FOR_ARBITRARY():
    country = "Arbitrary"
    progressive = True
    plotter = PLOT_POP_STAT(country,progressive)
    plotter.run()
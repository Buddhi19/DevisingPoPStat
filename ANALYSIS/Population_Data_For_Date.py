"""
NOT YET FULLY IMPLEMENTED
    ISSUES : Country names in the population data and COVID data are not matching.
           : Population data has other data like population of ASIA, EUROPE, etc.
           : ratawal hoyaganna. age data wala duplicates ain karanna 
"""
import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import COUNTRIES

age_data = pd.read_csv('Data\\population_data_with_age\\age_data.csv', low_memory = False)
saving_dir = os.path.join(main_dir, "Data\\population_data")

AGE_BRACKETS = 21

def POPULATION_DATA_FOR_DATE(date):
    data = age_data[age_data['Time'] == int(date)]
    for country in COUNTRIES:
        data_new = data[data['Location'].str.lower() == country]
        
        data_new = data_new.drop(columns = ['LocID'])
        data_new = data_new.drop_duplicates()

        data_new = data_new[['PopMale', 'PopFemale', 'PopTotal']]
        data_new.rename(columns = {'PopMale':'male', 'PopFemale':'female', 'PopTotal':'total'}, inplace = True)

        data_new.to_csv(os.path.join(saving_dir, f'{country}_population_data.csv'), index = False)
        print(f"{country} data saved successfully for {date}")
        

YEAR_AS_PER_PAPER = '2020'

if __name__ == "__main__":
    date = input(f"YEAR in YYYY or Press Enter to set year as {YEAR_AS_PER_PAPER} : ")
    if date == "":
        date = YEAR_AS_PER_PAPER
    POPULATION_DATA_FOR_DATE(date)

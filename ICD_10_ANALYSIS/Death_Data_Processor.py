import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

import pandas as pd
import re

from ICD_10_ANALYSIS.Country_Map import get_country, get_code
from ANALYSIS.COUNTRIES import mapping_name

DEATH_DATA_PATH = os.path.join(main_dir, 'ICD-10-DATA', 'Death_Data', 'Morticd10_part5_rev.csv')
POPULATION_DATA_DIR_PATH = os.path.join(main_dir, 'DATA', 'population_data_by_country')

DEATH_DATA = pd.read_csv(DEATH_DATA_PATH, low_memory=False)

MAIN_DISEASE_CATEGORIES = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N",
    "O","P","Q","R","S","T","U","V","W","X","Y","Z"
]

def get_total_population(country:str):
    POP_DATA = pd.read_csv(os.path.join(POPULATION_DATA_DIR_PATH, f'{country}_population.csv'))
    total_population = POP_DATA['total'].sum()
    return total_population


def DEATH_DATA_PROCESSOR(year:int):
    death_data = DEATH_DATA[DEATH_DATA['Year'] == year]
    DEATH_DATA_DATAFRAME = {
        'Country': [],
        'Country Code': [],
        'Cause Code' : [],
        'Deaths' : [],
        'Deaths per Million' : []
    }
    for country_code in death_data['Country'].unique():
        country_name = get_country(country_code)
        country_name_mapped = mapping_name(country_name)
        if country_name_mapped is None:
            continue
        total_population = get_total_population(country_name_mapped)
        country_data = death_data[death_data['Country'] == country_code]
        for cause_code in country_data['Cause'].unique():
            cause_data = country_data[country_data['Cause'] == cause_code]
            deaths = cause_data['Deaths1'].sum()
            deaths_per_million = (deaths / total_population)
            DEATH_DATA_DATAFRAME['Country'].append(country_name_mapped)
            DEATH_DATA_DATAFRAME['Country Code'].append(country_code)
            DEATH_DATA_DATAFRAME['Cause Code'].append(cause_code)
            DEATH_DATA_DATAFRAME['Deaths'].append(deaths)
            DEATH_DATA_DATAFRAME['Deaths per Million'].append(deaths_per_million)
        
    DEATH_DATA_DATAFRAME = pd.DataFrame(DEATH_DATA_DATAFRAME)
    DEATH_DATA_DATAFRAME.to_csv(os.path.join(main_dir, 'ICD-10-DATA', 'Death_Data', f'Death_Data_{year}.csv'), index=False)

def DEATH_DATA_PROCESSOR_BY_DISEASE(year:int):
    saved_data_path = os.path.join(main_dir, 'ICD-10-DATA', 'Death_Data', f'Death_Data_{year}.csv')
    if not os.path.exists(saved_data_path):
        DEATH_DATA_PROCESSOR(year)
    DEATH_DATA = pd.read_csv(saved_data_path)
    DATAFRAME = {
        'Country': [],
        'Country Code': [],
        'Cause Code' : [],
        'Deaths' : [],
        'Deaths per Million' : []
    }
    for country in DEATH_DATA['Country'].unique():
        country_data = DEATH_DATA[DEATH_DATA['Country'] == country]
        for disease in MAIN_DISEASE_CATEGORIES:
            disease_data = country_data[country_data['Cause Code'].str.startswith(disease)]
            disease_data = disease_data[disease_data['Cause Code'] != "AAA"]
            if disease_data.empty:
                continue
            deaths = disease_data['Deaths'].sum()
            deaths_per_million = disease_data['Deaths per Million'].sum()
            DATAFRAME['Country'].append(country)
            DATAFRAME['Country Code'].append(disease_data['Country Code'].values[0])
            DATAFRAME['Cause Code'].append(disease)
            DATAFRAME['Deaths'].append(deaths)
            DATAFRAME['Deaths per Million'].append(deaths_per_million)

    DATAFRAME = pd.DataFrame(DATAFRAME)
    DATAFRAME.to_csv(os.path.join(main_dir, 'ICD-10-DATA', 'Death_Data', f'Death_Data_By_Disease_{year}.csv'), index=False)
        

if __name__ == '__main__':
    # DEATH_DATA_PROCESSOR(2021)
    data = DEATH_DATA[DEATH_DATA['Year'] == 2021]
    list_of_countries = data['Country'].unique()
    print([get_country(x) for x in list_of_countries])    
    # DEATH_DATA_PROCESSOR_BY_DISEASE(2021)
    data = pd.read_csv(os.path.join(main_dir, 'ICD-10-DATA', 'Death_Data', 'Death_Data_2021.csv'))
    list_of_countries = data['Country'].unique()
    print(list_of_countries)
    print(len(list_of_countries))
    
        


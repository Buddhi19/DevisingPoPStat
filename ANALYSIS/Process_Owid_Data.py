import os
import sys
import pandas as pd

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name

DATA_DIR = os.path.join(main_dir, 'DATA/owid_data')

GINI_INDEX_FILE = 'economic-inequality-gini-index.csv'
GDP_PER_CAPITA_FILE = 'gdp-per-capita.csv'
GNI_FILE = 'gross-national-income-per-capita.csv'
HDI_FILE = 'human-development-index.csv'
MEDIAN_AGE_FILE = 'median-age.csv'
POPULATION_DENSITY_FILE = 'population-density.csv'
SDI_FILE = 'sdi_data.csv'
UNIVERSAL_HEALTH_COVERAGE_FILE = 'universal-health-coverage-index.csv'
LIFE_EXPECTANCY_FILE = 'life-expectancy.csv'

SAVING_DIR = os.path.join(main_dir, 'DATA/owid_data_filtered')

DATA_FILES = [
    GINI_INDEX_FILE,
    GDP_PER_CAPITA_FILE,
    GNI_FILE,
    HDI_FILE,
    MEDIAN_AGE_FILE,
    POPULATION_DENSITY_FILE,
    LIFE_EXPECTANCY_FILE,
    UNIVERSAL_HEALTH_COVERAGE_FILE
]

def process_country_names():
    for data_file in DATA_FILES:
        data = pd.read_csv(os.path.join(DATA_DIR, data_file))
        NEW_DATAFRAME = {}
        for column in data.columns:
            NEW_DATAFRAME[column] = []
        for row in data.iterrows():
            country = row[1]['Entity']
            country = mapping_name(country)
            if not country:
                continue
            NEW_DATAFRAME['Entity'].append(country)
            for column in data.columns:
                if column == 'Entity':
                    continue
                NEW_DATAFRAME[column].append(row[1][column])
        NEW_DATAFRAME = pd.DataFrame(NEW_DATAFRAME)
        NEW_DATAFRAME.to_csv(os.path.join(SAVING_DIR, data_file), index=False)
    print('Data processed successfully')

if __name__ == '__main__':
    process_country_names()
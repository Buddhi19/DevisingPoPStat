import sys
import os

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

import pandas as pd

COUNTRY_CODES_PATH = os.path.join(main_dir, 'ICD-10-DATA', 'Population_Data','country_codes.csv')
COUNTRY_CODES = pd.read_csv(COUNTRY_CODES_PATH)

def get_country(country_code: int):
    country_name = COUNTRY_CODES[COUNTRY_CODES['country'] == country_code]['name'].values[0]
    return country_name

def get_code(country_name: str):
    country_code = COUNTRY_CODES[COUNTRY_CODES['name'] == country_name]['country'].values[0]
    return country_code

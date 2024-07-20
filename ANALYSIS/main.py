import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

COUNTRY_DATA_PATH = os.path.join(main_dir, 'Data\\countries\\country_names.csv')

def construct_countries():
    data = pd.read_csv(COUNTRY_DATA_PATH).iloc[:, 0]
    countries = []
    for country in data:
        if not country:
            continue
        countries.append(country.lower())

    with open(os.path.join(main_dir, 'ANALYSIS\\COUNTRIES.py'), 'w') as f:
        f.write(f'COUNTRIES = {countries}')

if __name__ == "__main__":
    construct_countries()
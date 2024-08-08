import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name

owid_covid_data = pd.read_csv('Data\\owid_covid_data\\owid-covid-data.csv', low_memory = False)
saving_dir = os.path.join(main_dir, "Data\\covid_data_by_country")


def COVID_DATA_FOR_DATE(date):
    count = 0
    data_per_date = owid_covid_data[owid_covid_data['date'] == date]
    for country in data_per_date['location'].unique():
        data_per_country = data_per_date[data_per_date['location'] == country]
        pre_name = country
        country = mapping_name(country)
        if country is None:
            print(f"Country not found in the mapping : {pre_name}")
            continue
        data_per_country.to_csv(os.path.join(saving_dir, f'{country.lower()}_covid_data.csv'), index = False)
        print(f"{count}:{country} data saved successfully for {date}")
        count += 1

DATE_AS_PER_PAPER = '2022-04-08'

if __name__ == "__main__":
    date = input(f"Date in YYYY-MM-DD or Press Enter to set date as {DATE_AS_PER_PAPER} : ")
    if date == "":
        date = DATE_AS_PER_PAPER
    COVID_DATA_FOR_DATE(date)
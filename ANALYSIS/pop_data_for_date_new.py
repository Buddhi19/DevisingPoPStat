import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import COUNTRIES

saving_dir = os.path.join(main_dir, "Data\\pop_data_resolved")

age_data = pd.read_csv('Data\\population_data_with_age\\age_data.csv', low_memory = False)

def remove_duplicates(df):
    '''
    Removes duplicates
    Used after removing LocIDs from age_data.csv to remove identical rows
    '''
    return df.drop_duplicates(inplace = True)

def remove_column(df, col):
    '''
    Removes a given column of a dataframe.
    Used to remove LocID from age_data.csv since there were some duplicates with different LocIDs.
    '''
    return df.drop(columns = [col], axis = 1, inplace = True)

def make_country_data(df,year):
    '''
    Makes a csv file containing PopMale, PopFemale, PopTotal for every country separately for a given year
    '''
    male = []
    female = []
    tot = []
    for ind, row in df.iterrows():
        if '/' in row['Location']: # Removing Locations with '/'s. eg: Australia/New Zealand.
            parts = row['Location'].split('/')
            row['Location'] = parts[-1]
        if row['Time'] == year:
            male.append(row['PopMale'])
            female.append(row['PopFemale'])
            tot.append(row['PopTotal'])
        if row['Time'] == year and row['AgeGrp'] == '100+':
            country_data = {'male':male, 'female':female, 'total':tot}
            df = pd.DataFrame(country_data)
            df.to_csv(os.path.join(saving_dir, f"{row['Location']}_data.csv"), index=False)
            male = []
            female = []
            tot = []

if __name__ == "__main__":
    remove_column(age_data, 'LocID')
    remove_duplicates(age_data)
    year = int(input("Enter a year: "))
    make_country_data(age_data, year)
        


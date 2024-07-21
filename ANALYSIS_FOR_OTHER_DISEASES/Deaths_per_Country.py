"""
Not Fully Implemented Yet   
Dataset couldn't be found, previous processed data is used instead
"""
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

death_data = pd.read_csv("DATA/deaths_by_cause/deaths_by_cause.csv")

SAVING_PATH = "DATA/deaths_by_cause_per_country/"

start_year = 2018
end_year = 2019

death_data = death_data[death_data["Year"].between(start_year, end_year)]

ALL_CAUSES = death_data["Causes name"].unique()

DATA_FRAME = pd.DataFrame(columns=["Code"] + list(ALL_CAUSES))

COUNTRY_CODES = {}

row = 1
for country_code in death_data["Code"].unique():
    try:
        country_name = death_data[death_data["Code"] == country_code]["Entity"].iloc[0]
    except:
        print(country_code)
        continue
    COUNTRY_CODES[country_name] = [country_code]
    DATA_FRAME.loc[row, "Code"] = country_code
    for cause in ALL_CAUSES:
        DEATHS = 0
        for year in range(start_year, end_year + 1):
            DEATHS += death_data[(death_data["Code"] == country_code) & (death_data["Year"] == year) & (
                death_data["Causes name"] == cause)]["Death Numbers"].sum()
        DATA_FRAME.loc[row, cause] = DEATHS
    row += 1

population_data = pd.read_csv("DATA/population_data_with_age/age_data.csv")

population_data = population_data[population_data["Year"].between(start_year, end_year)]    
population_data = population_data.iloc[:, 1:]
population_data = population_data.drop_duplicates()

DATA_FRAME.to_csv(SAVING_PATH + "Deaths_per_Country.csv", index=False)
print(COUNTRY_CODES)
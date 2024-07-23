import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

COUNTRY_DATA = pd.read_csv("DATA/countries/country_names_map.csv")

def mapping_name(name:str):
    name = name.lower()
    if name in COUNTRY_DATA['death_data'].values:
        name = COUNTRY_DATA[COUNTRY_DATA['death_data'] == name]['Country'].values[0]
    elif name in COUNTRY_DATA["location"].values:
        name = COUNTRY_DATA[COUNTRY_DATA['location'] == name]['Country'].values[0]
    elif name not in COUNTRY_DATA['Country'].values:
        return None
    return name

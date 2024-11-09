import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

import pandas as pd


death_data_path = os.path.join(main_dir, "DATA", "death_data", "DEATH_DATA.csv")
death_data_path_for_span = os.path.join(main_dir, "DATA", "death_data", "DEATH_DATA_FOR_SPAN.csv")
population_data_path = os.path.join(main_dir, "DATA", "population_data_with_age", "age_data.csv")
hdi_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "human-development-index.csv")
median_age_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "median-age.csv")
gdp_per_capita_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "gdp-per-capita.csv")
population_density_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "population-density.csv")
sdi_data_path = os.path.join(main_dir, "DATA", "owid_data", "sdi_data.csv")
GINI_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "economic-inequality-gini-index.csv")
universal_health_coverage_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "universal-health-coverage-index.csv")
life_expectancy_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "life-expectancy.csv")

POPULATION_DATA = pd.read_csv(population_data_path, low_memory=False)
HDI_DATA = pd.read_csv(hdi_data_path, low_memory=False)
MEDIAN_AGE_DATA = pd.read_csv(median_age_data_path, low_memory=False)
GDP_PER_CAPITA_DATA = pd.read_csv(gdp_per_capita_data_path, low_memory=False)
POPULATION_DENSITY = pd.read_csv(population_density_path, low_memory=False)
SDI_DATA = pd.read_csv(sdi_data_path, encoding="ISO-8859-1", low_memory=False)
GINI_DATA = pd.read_csv(GINI_data_path, low_memory=False)
UHCI_DATA = pd.read_csv(universal_health_coverage_path, low_memory=False)
LIFE_EXPECTANCY_DATA = pd.read_csv(life_expectancy_path, low_memory=False)

SAVING_PATH_PNG = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "POPSTAT")
SAVING_PATH_PNG_HDI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "HDI")
SAVING_PATH_PNG_MEDIAN_AGE = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "MEDIAN_AGE")
SAVING_PATH_PNG_GDP_PER_CAPITA = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "GDP_PER_CAPITA")
SAVING_PATH_PNG_POPULATION_DENSITY = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "POPULATION_DENSITY")
SAVING_PATH_CSV = os.path.join(main_dir, "RESULTS", "CORRELATION_DATA_FOR_OTHER_DISEASES")
SAVING_PATH_PNG_SDI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "SDI")
SAVING_PATH_PNG_GINI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "GINI")
SAVING_PATH_PNG_UHCI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "UHCI")
SAVING_PATH_PNG_LIFE_EXPECTANCY = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "LIFE_EXPECTANCY")

COVID_DATA_DIR = os.path.join(main_dir, "DATA", "covid_data_by_country")
POPSTAT_COVID_DATA_DIR = os.path.join(main_dir, "RESULTS", "POPSTAT_COUNTRY_DATA")
POPSTAT_DISEASE_DATA_DIR = os.path.join(main_dir, "RESULTS", "POPSTAT_OTHER_DISEASES")

FOR_UI_PATH = os.path.join(main_dir, "RESULTS", "FOR_UI")

def SAVING_PATH_PNG_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "POPSTAT")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_HDI_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "HDI")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_MEDIAN_AGE_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "MEDIAN_AGE")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_GDP_PER_CAPITA_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "GDP_PER_CAPITA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_POPULATION_DENSITY_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "POPULATION_DENSITY")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_SDI_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "SDI")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_GINI_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "GINI")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_UHCI_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "UHCI")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_PNG_LIFE_EXPECTANCY_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_WITH_OTHER_DISEASES_{year}", "OTHER_METRICS", "LIFE_EXPECTANCY")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def SAVING_PATH_CSV_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"CORRELATION_DATA_FOR_OTHER_DISEASES_{year}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def FOR_UI_PATH_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"FOR_UI_{year}","DEATH_DATA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def FOR_UI_POPSTAT_PATH_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"FOR_UI_{year}","POPSTAT_COUNTRY_DATA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def FOR_UI_PYRAMIDS_PATH_FOR_YEAR(year:str):
    path = os.path.join(main_dir, "RESULTS", f"FOR_UI_{year}","PYRAMIDS")
    if not os.path.exists(path):
        os.makedirs(path)
    return path
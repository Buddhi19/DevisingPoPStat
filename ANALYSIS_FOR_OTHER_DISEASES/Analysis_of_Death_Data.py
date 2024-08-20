import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name

death_data_path = os.path.join(main_dir, "DATA", "death_data", "DEATH_DATA.csv")
population_data_path = os.path.join(main_dir, "DATA", "population_data_with_age", "age_data.csv")
hdi_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "human-development-index.csv")
median_age_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "median-age.csv")
gdp_per_capita_data_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "gdp-per-capita.csv")
population_density_path = os.path.join(main_dir, "DATA", "owid_data_filtered", "population-density.csv")
sdi_data_path = os.path.join(main_dir, "DATA", "owid_data", "sdi_data.csv")

DEATH_DATA = pd.read_csv(death_data_path, low_memory=False)
POPULATION_DATA = pd.read_csv(population_data_path, low_memory=False)
HDI_DATA = pd.read_csv(hdi_data_path, low_memory=False)
MEDIAN_AGE_DATA = pd.read_csv(median_age_data_path, low_memory=False)
GDP_PER_CAPITA_DATA = pd.read_csv(gdp_per_capita_data_path, low_memory=False)
POPULATION_DENSITY = pd.read_csv(population_density_path, low_memory=False)
SDI_DATA = pd.read_csv(sdi_data_path, encoding="ISO-8859-1", low_memory=False)

SAVING_PATH_PNG = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "POPSTAT")
SAVING_PATH_PNG_HDI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "HDI")
SAVING_PATH_PNG_MEDIAN_AGE = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "MEDIAN_AGE")
SAVING_PATH_PNG_GDP_PER_CAPITA = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "GDP_PER_CAPITA")
SAVING_PATH_PNG_POPULATION_DENSITY = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "POPULATION_DENSITY")
SAVING_PATH_CSV = os.path.join(main_dir, "RESULTS", "CORRELATION_DATA_FOR_OTHER_DISEASES")
SAVING_PATH_PNG_SDI = os.path.join(main_dir, "RESULTS", "CORRELATION_WITH_OTHER_DISEASES", "OTHER_METRICS", "SDI")

COVID_DATA_DIR = os.path.join(main_dir, "DATA", "covid_data_by_country")
POPSTAT_COVID_DATA_DIR = os.path.join(main_dir, "RESULTS", "POPSTAT_COUNTRY_DATA")
POPSTAT_DISEASE_DATA_DIR = os.path.join(main_dir, "RESULTS", "POPSTAT_OTHER_DISEASES", "Meningitis")

class MORTALITY_DATA:
    def __init__(self, year, country):
        self.REFERENCE_COUNTRY = country
        self.POPSTAT_COVID_DATA = pd.read_csv(os.path.join(POPSTAT_DISEASE_DATA_DIR, f"{country}_POPSTAT_COVID19.csv"))
        self.year = year

        self.CORR_COEFFICIENT = {
            "Parameter": [],
            "Cause of Death": [],
            "r squared value": [],
            "CI": [],
            "p-value": []
        }
        self.HDI_DATA = HDI_DATA[HDI_DATA['Year'] == int(self.year)]

        self.MEDIAN_AGE_DATA = MEDIAN_AGE_DATA[MEDIAN_AGE_DATA['Year'] == int(self.year)]
        self.MEDIAN_AGE_DATA.columns = ["Entity", "Code", "Year", "Median Age", ""]

        self.GDP_per_capita_data = GDP_PER_CAPITA_DATA[GDP_PER_CAPITA_DATA['Year'] == int(self.year)]
        self.Pop_Density = POPULATION_DENSITY[POPULATION_DENSITY['Year'] == int(self.year)]

        if self.year <= 2019:
            self.SDI_data = SDI_DATA[["Location", str(self.year)]]

    def create_death_data_per_disease(self, disease, country):
        filtered_data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        filtered_data = filtered_data[filtered_data['location_name'] == country]
        year_data = filtered_data[(filtered_data['year'] == self.year)]
        total_death_rate = year_data[year_data['metric_name'] == 'Rate']
        if total_death_rate.empty:
            return None
        total_deaths = total_death_rate['val'].values[0]
        return total_deaths
    
    def create_dataframe_for_diseases(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.POPSTAT_COVID_DATA["Country"].values:
                continue
            popstat_val = self.POPSTAT_COVID_DATA[self.POPSTAT_COVID_DATA["Country"] == country]["POPSTAT_COVID19"].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(popstat_val)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease)

    def create_dataframe_for_diseases_HDI(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.HDI_DATA['Entity'].str.lower().values:
                continue
            HDI = self.HDI_DATA[self.HDI_DATA['Entity'].str.lower() == country]['Human Development Index'].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(HDI)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_HDI, variable = "HDI")

    def create_dataframe_for_diseases_SDI(self, disease):
        if self.year > 2019:
            return
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in SDI_DATA['Location'].str.lower().values:
                continue
            SDI = SDI_DATA[SDI_DATA['Location'].str.lower() == country][str(self.year)].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(SDI)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_SDI, variable = "SDI")

    def create_dataframe_for_diseases_MEDIAN_AGE(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.MEDIAN_AGE_DATA['Entity'].str.lower().values:
                continue
            median_age = self.MEDIAN_AGE_DATA[self.MEDIAN_AGE_DATA['Entity'].str.lower() == country]['Median Age'].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(median_age)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_MEDIAN_AGE, variable = "Median Age")
    
    def create_dataframe_for_diseases_GDP_PER_CAPITA(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.GDP_per_capita_data['Entity'].str.lower().values:
                continue
            GDP_per_capita = self.GDP_per_capita_data[self.GDP_per_capita_data['Entity'].str.lower() == country]['GDP per capita'].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(GDP_per_capita)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_GDP_PER_CAPITA, variable = "GDP per capita")

    def create_dataframe_for_diseases_POPULATION_DENSITY(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.Pop_Density['Entity'].str.lower().values:
                continue
            Pop_Density = self.Pop_Density[self.Pop_Density['Entity'].str.lower() == country]['Population density'].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(disease, pre_name)
            if not total_deaths_per_million:
                continue
            X.append(Pop_Density)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_POPULATION_DENSITY, variable = "Population Density")

    def PLOT(self, X, Y, title, saving_path=SAVING_PATH_PNG,variable = "POPSTAT_COVID19"):
        X = np.array(X)
        Y = np.array(Y)
        mask = (Y > 0)
        X = X[mask]
        Y = Y[mask]
        Y = np.log(Y)
        mask = np.isfinite(Y)
        X = X[mask]
        Y = Y[mask] 
        if len(X) < 2 or len(Y) < 2:
            return
        plt.scatter(X, Y)
        plt.xlabel(f"{variable}")
        plt.ylabel(f"{title} Deaths/Log")

        correalation_coefficient, p_value = stats.pearsonr(X, Y)
        r_squared = correalation_coefficient ** 2

        n = len(X)
        r_z = np.arctanh(correalation_coefficient)
        se = 1/np.sqrt(n-3)
        z = stats.norm.ppf((1+0.95)/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))

        print(f"R² = {r_squared:.3f} for {title} deaths")
        print(f"Correlation coefficient = {correalation_coefficient:.3f} for {title} deaths")
        print(f"95% confidence interval: {lo:.3f} to {hi:.3f} for {title} deaths")
        print(f"p-value = {p_value:.6f} for {title} deaths")

        self.CORR_COEFFICIENT['Parameter'].append(variable)
        self.CORR_COEFFICIENT['Cause of Death'].append(title)
        self.CORR_COEFFICIENT['r squared value'].append(r_squared)
        self.CORR_COEFFICIENT['CI'].append((lo, hi))
        self.CORR_COEFFICIENT['p-value'].append(p_value)

        z = np.polyfit(X, Y, 1)
        p = np.poly1d(z)
        plt.plot(X, p(X), "r--")

        plt.text(0.05, 0.95, f'R² = {r_squared:.3f}',
                        transform=plt.gca().transAxes, verticalalignment='top')
        title = title.replace("/", "")
        plt.savefig(os.path.join(saving_path, f'{title}_deaths.png'))
        plt.close()

        print(f"Data for {title} has been plotted with {len(X)} countries for {variable}")
        print()

    def ANALYZER(self):
        for disease in DEATH_DATA['cause_name'].unique():
            self.create_dataframe_for_diseases(disease)
            self.create_dataframe_for_diseases_HDI(disease)
            self.create_dataframe_for_diseases_MEDIAN_AGE(disease)
            self.create_dataframe_for_diseases_GDP_PER_CAPITA(disease)
            self.create_dataframe_for_diseases_POPULATION_DENSITY(disease)
            self.create_dataframe_for_diseases_SDI(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_{self.REFERENCE_COUNTRY}.csv"))

    def ANALYZER_FOR_SELECTED_DISEASES(self):
        diseases = [
            "Cardiovascular diseases",
            "Acute hepatitis",
            "Meningitis",
            "Maternal disorders",
            "Nutritional deficiencies",
            "Tuberculosis",
            "Neonatal disorders",
            "Parkinson's disease",
            "Alzheimer's disease and other dementias",
            "HIV/AIDS",
            "Malaria",
            "Diarrheal diseases",
            "Neoplasms",
            "Protein-energy malnutrition",
            "Chronic kidney disease",
            "Chronic respiratory diseases",
            "Cirrhosis and other chronic liver diseases",
            "Diabetes mellitus",
            "Digestive diseases",
            "Lower respiratory infections",
            "Conflict and terrorism",
            "Drowning",
            "Drug use disorders",
            "Environmental heat and cold exposure",
            "Exposure to forces of nature"
        ]
        for disease in diseases:
            self.create_dataframe_for_diseases(disease)
            self.create_dataframe_for_diseases_GDP_PER_CAPITA(disease)
            self.create_dataframe_for_diseases_HDI(disease)
            self.create_dataframe_for_diseases_MEDIAN_AGE(disease)
            self.create_dataframe_for_diseases_POPULATION_DENSITY(disease)
            self.create_dataframe_for_diseases_SDI(disease)

        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_{self.REFERENCE_COUNTRY}_JS.csv"))


if __name__ == "__main__":
    data = MORTALITY_DATA(2021, "moldova")
    data.ANALYZER_FOR_SELECTED_DISEASES()
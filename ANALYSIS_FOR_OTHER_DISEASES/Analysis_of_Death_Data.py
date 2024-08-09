import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYSIS.COUNTRIES import mapping_name

DEATH_DATA = pd.read_csv("DATA/death_data/deaths_by_cause.csv", low_memory=False)
POPULATION_DATA = pd.read_csv("DATA/population_data_with_age/age_data.csv", low_memory=False)
HDI_DATA = pd.read_csv("DATA/owid_data/human-development-index.csv", low_memory=False)
MEDIAN_AGE_DATA = pd.read_csv("DATA/owid_data/median-age.csv", low_memory=False)

SAVING_PATH_PNG = "RESULTS/CORRELATION_WITH_OTHER_DISEASES/POPSTAT"
SAVING_PATH_PNG_HDI = "RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/HDI"
SAVING_PATH_PNG_MEDIAN_AGE = "RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/MEDIAN_AGE"
SAVING_PATH_PNG_GDP_PER_CAPITA = "RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/GDP_PER_CAPITA"
SAVING_PATH_PNG_POPULATION_DENSITY = "RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/POPULATION_DENSITY"
SAVING_PATH_CSV = "RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES"

COVID_DATA_DIR = "DATA/covid_data_by_country"
POPSTAT_COVID_DATA_DIR = "RESULTS/POPSTAT_COUNTRY_DATA"

class MORTALITY_DATA:
    def __init__(self, year, country):
        self.POPSTAT_COVID_DATA = pd.read_csv(os.path.join(POPSTAT_COVID_DATA_DIR, f"{country}_POPSTAT_COVID19.csv"))
        self.year = year

        self.COUNTRY_DATA = {
            "Country": [],
            "Population": []
        }
        self.create_population_data()
        self.CORR_COEFFICIENT = {
            "Cause of Death": [],
            "Correlation Coefficient": [],
            "CI": [],
            "p-value": []
        }
        self.HDI_DATA = HDI_DATA[HDI_DATA['Year'] == int(self.year)]

        self.MEDIAN_AGE_DATA = MEDIAN_AGE_DATA[MEDIAN_AGE_DATA['Year'] == int(self.year)]
        self.MEDIAN_AGE_DATA.columns = ["Entity", "Code", "Year", "Median Age", ""]

    def create_population_data(self):
        for country in POPULATION_DATA['Location'].unique():
            pop_data = POPULATION_DATA[POPULATION_DATA['Location'] == country]
            pop_data = pop_data.drop(columns=['LocID'])
            pop_data = pop_data.drop_duplicates()
            pop_data = pop_data[pop_data['Time'] == int(self.year)]
            total_population = pop_data['PopTotal'].sum()
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            self.COUNTRY_DATA['Country'].append(country)
            self.COUNTRY_DATA['Population'].append(total_population)

    def create_death_data_per_disease(self, disease, country):
        filtered_data = DEATH_DATA[DEATH_DATA['Causes name'] == disease]
        filtered_data = filtered_data[filtered_data['Entity'] == country]
        year_data = filtered_data[(filtered_data['Year'] == self.year)]
        total_deaths = year_data['Death Numbers'].values[0]
        return total_deaths
    
    def create_dataframe_for_diseases(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['Causes name'] == disease]
        for country in data['Entity'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.POPSTAT_COVID_DATA["Country"].values:
                continue
            popstat_val = self.POPSTAT_COVID_DATA[self.POPSTAT_COVID_DATA["Country"] == country]["POPSTAT_COVID19"].values[0]
            X.append(popstat_val)
            total_deaths = self.create_death_data_per_disease(disease, pre_name)
            population = self.COUNTRY_DATA['Population'][self.COUNTRY_DATA['Country'].index(country)]
            Y.append(total_deaths/population)

        self.PLOT(X,Y, disease)
        print(f"Data for {disease} has been plotted")

    def create_dataframe_for_diseases_HDI(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['Causes name'] == disease]
        for country in data['Entity'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.HDI_DATA['Entity'].str.lower().values:
                continue
            HDI = self.HDI_DATA[self.HDI_DATA['Entity'].str.lower() == country]['Human Development Index'].values[0]
            X.append(HDI)
            total_deaths = self.create_death_data_per_disease(disease, pre_name)
            population = self.COUNTRY_DATA['Population'][self.COUNTRY_DATA['Country'].index(country)]
            Y.append(total_deaths/population)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_HDI, variable = "HDI")
        print(f"Data for {disease} has been plotted with HDI")

    def create_dataframe_for_diseases_MEDIAN_AGE(self, disease):
        X = []
        Y = []
        data = DEATH_DATA[DEATH_DATA['Causes name'] == disease]
        for country in data['Entity'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.MEDIAN_AGE_DATA['Entity'].str.lower().values:
                continue
            median_age = self.MEDIAN_AGE_DATA[self.MEDIAN_AGE_DATA['Entity'].str.lower() == country]['Median Age'].values[0]
            X.append(median_age)
            total_deaths = self.create_death_data_per_disease(disease, pre_name)
            population = self.COUNTRY_DATA['Population'][self.COUNTRY_DATA['Country'].index(country)]
            Y.append(total_deaths/population)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_MEDIAN_AGE, variable = "Median Age")
        print(f"Data for {disease} has been plotted with Median Age")

    
    def create_dataframe_for_diseases_GDP_PER_CAPITA(self, disease):
        pass
            

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

        self.CORR_COEFFICIENT['Cause of Death'].append(title)
        self.CORR_COEFFICIENT['Correlation Coefficient'].append(correalation_coefficient)
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

    def ANALYZER(self):
        for disease in DEATH_DATA['cause_name'].unique():
            self.create_dataframe_for_diseases(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, "Correlation_Coefficient.csv"))

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
            self.create_dataframe_for_diseases_HDI(disease)
            self.create_dataframe_for_diseases_MEDIAN_AGE(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, "Correlation_Coefficient.csv"))


if __name__ == "__main__":
    data = MORTALITY_DATA(2018, "japan")
    data.ANALYZER_FOR_SELECTED_DISEASES()
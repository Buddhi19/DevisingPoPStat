import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYSIS.COUNTRIES import mapping_name

DEATH_DATA = pd.read_csv("DATA/death_data/death_data.csv", low_memory=False)
POPULATION_DATA = pd.read_csv("DATA/population_data_with_age/age_data.csv", low_memory=False)
POPSTAT_COVID_DATA = pd.read_csv("RESULTS/POPSTAT_COUNTRY_DATA/japan_POPSTAT_COVID19.csv")

SAVING_PATH_PNG = "RESULTS/CORRELATION_WITH_OTHER_DISEASES"
SAVING_PATH_CSV = "RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES"

COVID_DATA_DIR = "DATA/covid_data_by_country"

class MORTALITY_DATA:
    def __init__(self, year):
        if isinstance(year, int):
            self.years = [year]
        elif isinstance(year, list):
            self.years =year

        self.COUNTRY_DATA = {
            "Country": [],
            "Average Population": [],
            "Median Age": [],
            "GDP per Capita": [],
            "Population Density": []
        }
        self.create_population_data()
        self.CORR_COEFFICIENT = {
            "Cause of Death": [],
            "Correlation Coefficient": [],
            "CI": [],
            "p-value": []
        }

    @classmethod
    def ADD_RANGE(cls, start, end):
        years = list(range(start, end + 1))
        return cls(years)
    
    def create_population_data(self):
        for country in POPULATION_DATA['Location'].unique():
            pop_data = POPULATION_DATA[POPULATION_DATA['Location'] == country]
            pop_data = pop_data.drop(columns=['LocID'])
            pop_data = pop_data.drop_duplicates()
            total_population = 0
            for year in self.years:
                pop_data = pop_data[pop_data['Time'] == int(year)]
                total_population += pop_data['PopTotal'].sum()

            self.average_population = total_population / len(self.years)
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            self.COUNTRY_DATA['Country'].append(country)
            self.COUNTRY_DATA['Average Population'].append(self.average_population)

    def create_death_data_per_disease(self, disease, country):
        filtered_data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        filtered_data = filtered_data[filtered_data['location_name'] == country]
        total_deaths = 0
        for year in self.years:
            year_data = filtered_data[(filtered_data['year'] == year) & 
                          (filtered_data['age_name'] == 'All ages') & 
                          (filtered_data['sex_name'] == 'Both')]
            total_deaths += year_data['val'].sum()

        self.average_deaths = total_deaths / len(self.years)
        return self.average_deaths
    
    def create_dataframe_for_diseases(self, disease):
        DATAFRAME = {
            'Country': [],
            'Average Population': [],
            'Average Deaths': [],
            'Deaths per million': [],
            'POPSTAT Data': [],
        }
        data = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in POPSTAT_COVID_DATA["Country"].values:
                continue
            popstat_val = POPSTAT_COVID_DATA[POPSTAT_COVID_DATA["Country"] == country]["POPSTAT_COVID19"].values[0]
            DATAFRAME['POPSTAT Data'].append(popstat_val)
            average_deaths = self.create_death_data_per_disease(disease, pre_name)
            DATAFRAME['Average Deaths'].append(average_deaths)
            DATAFRAME['Country'].append(country)
            average_population = self.COUNTRY_DATA['Average Population'][self.COUNTRY_DATA['Country'].index(country)]
            DATAFRAME['Average Population'].append(average_population)
            DATAFRAME['Deaths per million'].append(average_deaths / average_population)

        self.PLOT_WITH_POPSTAT(DATAFRAME['POPSTAT Data'], DATAFRAME['Deaths per million'], disease)
        print(f"Data for {disease} has been plotted")

    def PLOT_WITH_POPSTAT(self, X, Y, title, saving_path=SAVING_PATH_PNG):
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
        plt.xlabel("POPSTAT_COVID19")
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
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, "Correlation_Coefficient.csv"))


if __name__ == "__main__":
    data = MORTALITY_DATA.ADD_RANGE(2018, 2020)
    data.ANALYZER()
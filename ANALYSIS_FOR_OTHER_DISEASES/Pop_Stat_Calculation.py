import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS_FOR_OTHER_DISEASES.Death_data_Processor import DEATH_DATA_PROCESSOR


DEATH_DATA_PATH = os.path.join(main_dir,"DATA/death_data/DEATH_DATA.csv")

POPULATION_DIR = os.path.join(main_dir, 'DATA/population_data_by_country')
RESULTS_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_OTHER_DISEASES')

class POP_STAT_CALCULATION_FOR_OTHER_DISEASES(POP_STAT_CALCULATION):
    def __init__(self, disease, year):
        super().__init__()
        self.CONSIDERING_COUNTRIES = 2
        self.disease = disease
        self.disease_data = {}
        DEATH_DATA = pd.read_csv(DEATH_DATA_PATH)
        self.DEATH_DATA = DEATH_DATA[DEATH_DATA['cause_name'] == disease]
        self.DEATH_DATA = self.DEATH_DATA[self.DEATH_DATA['year'] == year]

        for country in self.DEATH_DATA['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country is None:
                continue
            death_data_per_country = self.DEATH_DATA[self.DEATH_DATA['location_name'] == pre_name]
            death_data_per_country = death_data_per_country[death_data_per_country["metric_name"] == "Rate"]
            total_deaths_per_million = death_data_per_country["val"].values[0]
            self.disease_data[country] = total_deaths_per_million

        self.common_countries = set(self.population_data.keys() & self.disease_data.keys())

    def remove_nan_values(self):
        NAN_COUNTRIES = []
        for country, dist in self.population_data.items():
            if not np.isfinite(dist).all():
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite values found in population data for {country}")
        
        for country, value in self.disease_data.items():
            if not np.isfinite(value):
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite value found in {self.disease} data for {country}")

        if NAN_COUNTRIES:
            self.population_data = {country: dist for country, dist in self.population_data.items() if country not in NAN_COUNTRIES}
            self.disease_data = {country: value for country, value in self.disease_data.items() if country not in NAN_COUNTRIES}
    
    def run(self):
        self.remove_nan_values()
        self.reference_country = self.find_optimal_reference()
        return self.reference_country

    def POPSTAT_DISEASE(self, reference_country):
        return super().POPSTAT_COVID19(reference_country)

    @staticmethod
    def MASK(X, Y):
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
            return None, None
        return X, Y
    
    def find_optimal_reference(self):
        country_correlations = {}

        common_countries = set(self.population_data.keys()) & set(self.disease_data.keys())

        for reference_country in common_countries:
            distances = self.POPSTAT_DISEASE(reference_country)

            # countries_without_nan = [country for country in common_countries]

            common_distances = [distances[country] for country in common_countries]
            common_disease_data = [np.log(self.disease_data[country]) for country in common_countries]

            common_distances, common_disease_data = self.MASK(common_distances, common_disease_data)
            if common_distances is None or common_disease_data is None:
                country_correlations[reference_country] = 0
                continue

            correlation, _ = stats.pearsonr(common_distances, common_disease_data)
            country_correlations[reference_country] = correlation

        country_correlations = sorted(country_correlations, key = lambda x: abs(country_correlations[x]), reverse = True)
        if country_correlations[0] == 0:
            print(f"Warning: No correlation found for {self.disease} disease thus using Japan as reference")
            return 'japan'

        print(f"Optimal reference for {self.disease} disease is {country_correlations[0]}")
        return country_correlations[0]
        


if __name__ == "__main__":
    data = pd.read_csv(os.path.join(main_dir, 'DATA/death_data/DEATH_DATA.csv')) 
    diseases = data['cause_name'].unique()
    year = 2020
    DEATH_DATA_PROCESSOR(year)
    for disease in diseases:
        print(f"Calculating POPSTAT for {disease} disease")
        POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, year).run()
        print()
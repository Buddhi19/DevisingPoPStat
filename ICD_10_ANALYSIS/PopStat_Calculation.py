import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION


DEATH_DATA_DIR = os.path.join(main_dir, 'ICD-10-DATA/Death_Data')
POPULATION_DIR = os.path.join(main_dir, 'DATA/population_data_by_country')
RESULTS_DIR = os.path.join(main_dir, 'ICD-10-RESULTS')

class POP_STAT_CALCULATION_FOR_OTHER_DISEASES(POP_STAT_CALCULATION):
    def __init__(self, disease, year):
        super().__init__()
        self.CONSIDERING_COUNTRIES = 2
        self.disease = disease
        self.disease_data = {}
        DEATH_DATA = pd.read_csv(os.path.join(DEATH_DATA_DIR, f'Death_Data_By_Disease_{year}.csv'))
        self.DEATH_DATA = DEATH_DATA[DEATH_DATA['Cause Code'] == disease]

        for country in self.DEATH_DATA['Country'].unique():
            death_data_per_country = self.DEATH_DATA[self.DEATH_DATA['Country'] == country]
            total_deaths_per_million = death_data_per_country["Deaths per Million"].values[0]
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

            common_distances = [distances[country] for country in common_countries]
            common_disease_data = [self.disease_data[country] for country in common_countries]

            common_distances, common_disease_data = self.MASK(common_distances, common_disease_data)
            if common_distances is None or common_disease_data is None:
                country_correlations[reference_country] = 0
                continue

            correlation, _ = stats.pearsonr(common_distances, common_disease_data)
            country_correlations[reference_country] = correlation


        country_correlations = sorted(country_correlations.items(), key=lambda x: x[1], reverse=True)
        # print(country_correlations)

        if not country_correlations:
            print(f"Warning: No correlation found for {self.disease} disease thus using Japan as reference")
            return 'japan'

        print(f"Optimal reference for {self.disease} disease is {country_correlations[0][0]} with correlation {country_correlations[0][1]}")
        return country_correlations[0][0]
        

if __name__ == "__main__":
    for disease in [
        "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
    ]:
        pop_stat = POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, 2021)
        reference_country = pop_stat.run()
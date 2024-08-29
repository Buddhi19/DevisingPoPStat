import numpy as np
import pandas as pd
from scipy.stats import pearsonr, entropy
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

POPULATION_DIR = os.path.join(main_dir, 'DATA/population_data_by_country')
COVID_DIR = os.path.join(main_dir, 'DATA/covid_data_by_country')
RESULTS_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_COUNTRY_DATA')

class POP_STAT_CALCULATION:
    def __init__(self):
        self.CONSIDERING_COUNTRIES = 20
        self.population_data = {}
        for file_name in os.listdir(POPULATION_DIR):
            if not file_name.endswith('.csv'):
                continue
            country_name = file_name.split('_')[0]
            data = pd.read_csv(os.path.join(POPULATION_DIR, file_name))
            population_array = np.array(data['total']/data['total'].sum())
            self.population_data[country_name] = population_array

        self.covid_data = {}
        for file_name in os.listdir(COVID_DIR):
            if not file_name.endswith('.csv'):
                continue
            country_name = file_name.split('_')[0]
            data = pd.read_csv(os.path.join(COVID_DIR, file_name))
            total_deaths_per_million = data['total_deaths_per_million'].tolist()[0]
            total_cases_per_million = data['total_cases_per_million'].tolist()[0]
            self.covid_data[country_name] = total_deaths_per_million*1 

        """
        self.HDI_data = {}
        for file_name in os.listdir(COVID_DIR):
            if not file_name.endswith('.csv'):
                continue
            country_name = file_name.split('_')[0]
            data = pd.read_csv(os.path.join(COVID_DIR, file_name))
            HDI = data['human_development_index'].tolist()[0]
            self.HDI_data[country_name] = HDI
        """

        self.common_countries = set(self.population_data.keys()) & set(self.covid_data.keys())

    def run(self):
        self.remove_nan_values()
        self.progressive_reference_countries, self.regressive_reference_countries = self.find_optimal_reference()
        self.progressive_reference_countries = self.progressive_reference_countries[:self.CONSIDERING_COUNTRIES]
        self.regressive_reference_countries = self.regressive_reference_countries[:self.CONSIDERING_COUNTRIES]
        for country, correlation in self.progressive_reference_countries:
            self.create_POPSTAT_COVID19_data(country)
        for country, correlation in self.regressive_reference_countries:
            self.create_POPSTAT_COVID19_data(country)
        return self.progressive_reference_countries, self.regressive_reference_countries


    def create_POPSTAT_COVID19_data(self, reference_country):
        data = self.POPSTAT_COVID19(reference_country)
        data = pd.DataFrame(data.items(), columns = ['Country', 'POPSTAT_COVID19'])
        data.to_csv(os.path.join(RESULTS_DIR, f'{reference_country}_POPSTAT_COVID19.csv'), index = False)
        print(f"POPSTAT_COVID19 data saved successfully for {reference_country}")   


    def remove_nan_values(self):
        NAN_COUNTRIES = []
        for country, dist in self.population_data.items():
            if not np.isfinite(dist).all():
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite values found in population data for {country}")
        
        for country, value in self.covid_data.items():
            if not np.isfinite(value):
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite value found in COVID data for {country}")

        # for country, value in self.HDI_data.items():
        #     if not np.isfinite(value):
        #         NAN_COUNTRIES.append(country)
        #         print(f"Warning: Non-finite value found in HDI data for {country}")

        if NAN_COUNTRIES:
            self.population_data = {country: dist for country, dist in self.population_data.items() if country not in NAN_COUNTRIES}
            self.covid_data = {country: value for country, value in self.covid_data.items() if country not in NAN_COUNTRIES}
            # self.HDI_data = {country: value for country, value in self.HDI_data.items() if country not in NAN_COUNTRIES}

    @staticmethod
    def KL_DIVERGENCE(p, q):
        p = np.asarray(p)
        q = np.asarray(q)
        
        epsilon = 1e-10
        p = p + epsilon
        q = q + epsilon
        
        p = p / np.sum(p)
        q = q / np.sum(q)
        
        return np.sum(p * np.log(p / q))
    
    def JENSEN_SHANNON_DIVERGENCE(self,p, q):
        p = np.asarray(p)
        q = np.asarray(q)
        m = (p + q) / 2
        return (self.KL_DIVERGENCE(p, m) + self.KL_DIVERGENCE(q, m)) / 2
    
    @staticmethod
    def EUCLIDEAN_DISTANCE(p, q):
        p = np.asarray(p)
        q = np.asarray(q)

        return np.linalg.norm(p - q)

    def POPSTAT_COVID19(self,reference_country):
        print(f"Calculating POPSTAT_COVID19 for {reference_country}")
        reference_dist = self.population_data[reference_country]
        # HDI_reference = self.HDI_data[reference_country]
        distances = {}
        for country, dist in self.population_data.items():
            if country in self.common_countries:
                # HDI_country = self.HDI_data[country]
                distances[country] = self.KL_DIVERGENCE(dist, reference_dist)
        return distances

    def find_optimal_reference(self):
        country_correlations = {}

        common_countries = set(self.population_data.keys()) & set(self.covid_data.keys())

        for reference_country in common_countries:
            distances = self.POPSTAT_COVID19(reference_country)

            common_distances = [distances[country] for country in common_countries]
            common_covid_data = [self.covid_data[country] for country in common_countries]

            correlation = np.corrcoef(common_distances, common_covid_data)[0, 1]
            country_correlations[reference_country] = correlation

        country_correlations = sorted(country_correlations.items(), key = lambda x: abs(x[1]), reverse = True)
        country_correlations_progressive = sorted(country_correlations, key = lambda x: x[1], reverse = True)
        country_correlations_regressive = sorted(country_correlations, key = lambda x: x[1], reverse = False)

        print(f"Top {self.CONSIDERING_COUNTRIES} countries with highest correlation with progressive population distribution")
        for country, correlation in country_correlations_progressive[:self.CONSIDERING_COUNTRIES]:
            print(f"{country}: {correlation}")

        print()

        print(f"Top {self.CONSIDERING_COUNTRIES} countries with highest correlation with regressive population distribution")
        for country, correlation in country_correlations_regressive[:self.CONSIDERING_COUNTRIES]:
            print(f"{country}: {correlation}")

        return country_correlations_progressive, country_correlations_regressive


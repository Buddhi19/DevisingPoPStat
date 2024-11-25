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
DEATH_DATA_PATH_FOR_SPAN = os.path.join(main_dir,"DATA/death_data/DEATH_DATA_FOR_SPAN.csv")

POPULATION_DIR = os.path.join(main_dir, 'DATA/population_data_by_country')
RESULTS_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_OTHER_DISEASES')

class POP_STAT_CALCULATION_FOR_OTHER_DISEASES(POP_STAT_CALCULATION):
    def __init__(self, disease, year, singleMode = True):
        super().__init__()
        self.CONSIDERING_COUNTRIES = 4
        self.disease = disease
        self.disease_data = {}
        DEATH_DATA = pd.read_csv(DEATH_DATA_PATH) if singleMode else pd.read_csv(DEATH_DATA_PATH_FOR_SPAN)
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

        Confidence_intervals = {}
        P_values = {}
        MSE_loss = {}

        common_countries = set(self.population_data.keys()) & set(self.disease_data.keys())

        for reference_country in common_countries:
            distances = self.POPSTAT_DISEASE(reference_country)

            # countries_without_nan = [country for country in common_countries]

            common_distances = [distances[country] for country in common_countries]
            common_disease_data = [self.disease_data[country] for country in common_countries]

            common_distances, common_disease_data = self.MASK(common_distances, common_disease_data)
            if common_distances is None or common_disease_data is None:
                country_correlations[reference_country] = 0
                continue

            correlation, p_val = stats.pearsonr(common_distances, common_disease_data)

            n = len(common_distances)
            r_z = np.arctanh(correlation)
            se = 1/np.sqrt(n-3)
            z = stats.norm.ppf((1+0.95)/2)
            lo_z, hi_z = r_z-z*se, r_z+z*se
            lo, hi = np.tanh((lo_z, hi_z)) 

            Confidence_intervals[reference_country] = (lo, hi)
            P_values[reference_country] = p_val
            country_correlations[reference_country] = correlation

            y_pred = np.polyval(np.polyfit(common_distances, common_disease_data, 1), common_distances)
            MSE_loss[reference_country] = np.square(np.subtract(common_disease_data, y_pred)).mean()

        country_correlations = sorted(country_correlations.items(), key=lambda x: abs(x[1]), reverse=True)

        # return disease, country_correlations
        # self.save_results(self.disease, country_correlations, P_values, Confidence_intervals, MSE_loss)
        if not country_correlations:
            print(f"Warning: No correlation found for {self.disease} disease thus using Japan as reference")
            return 'japan'
        if country_correlations[0][1] == 0:
            print(f"Warning: No correlation found for {self.disease} disease thus using Japan as reference")
            return 'japan'

        print(f"Optimal reference for {self.disease} disease is {country_correlations[0][0]}")
        return country_correlations[0][0]
    
    def save_results(self,disease, country_correlations, P_values, Confidence_intervals, MSE_loss):
        self.DATAFRAME = {
            'Reference' : [],
            'Deaths per million' : [],
            'r squared val' : [],
            'r value' : [],
            'p value' : [],
            'Confidence Interval' : [],
            'MSE Loss' : []
        }
        for i in range(self.CONSIDERING_COUNTRIES):
            if i >= len(country_correlations):
                break
            self.DATAFRAME['Reference'].append(country_correlations[i][0])
            self.DATAFRAME['Deaths per million'].append(
                self.disease_data[country_correlations[i][0]]
            )
            self.DATAFRAME['r squared val'].append(country_correlations[i][1]**2)
            self.DATAFRAME['r value'].append(country_correlations[i][1])
            self.DATAFRAME['p value'].append(P_values[country_correlations[i][0]])
            self.DATAFRAME['Confidence Interval'].append(Confidence_intervals[country_correlations[i][0]])
            self.DATAFRAME['MSE Loss'].append(MSE_loss[country_correlations[i][0]])

        self.DATAFRAME = pd.DataFrame(self.DATAFRAME)
        disease = disease.replace('/', '_')
        self.DATAFRAME.to_csv(
            os.path.join(
                RESULTS_DIR,'MULTIPLE_REFERENCES', f'{self.CONSIDERING_COUNTRIES}_Best_References_for_{disease}.csv'
            ), index=False
        )

class UPDATE_RESULTS_FOR_OTHER_DISEASES:
    def __init__(self):
        self.CONSIDERING_COUNTRIES = 4
        self.save_results_for_dataset()
    
    def save_results_for_dataset(self):
        dataset = pd.read_csv(os.path.join(main_dir, 'RESULTS',"CORRELATION_DATA_FOR_OTHER_DISEASES",
                                           "Correlation_coefficient_selected.csv"))
        new_dataframe = {
            v : dataset[v].values for v in dataset.columns
        }
        for i in range(self.CONSIDERING_COUNTRIES):
            new_dataframe[f'Reference {i+2}'] = [None for _ in range(len(dataset))]

        self.new_dataframe = new_dataframe

    def update_new_dataframe(self,disease, country_correlations):
        index = self.new_dataframe['Disease'].tolist().index(disease)
        for i in range(self.CONSIDERING_COUNTRIES):
            if i >= len(country_correlations):
                break
            self.new_dataframe[f'Reference {i+2}'][index] = country_correlations[i][0]

    def save_new_dataframe(self):
        new_dataframe = pd.DataFrame(self.new_dataframe)
        new_dataframe.to_csv(
            os.path.join(
                main_dir,'RESULTS', 'CORRELATION_DATA_FOR_OTHER_DISEASES', 'Correlation_selected.csv'
            ), index=False
        )




if __name__ == "__main__":
    diseases = [
            "Ischemic heart disease",
            "Stroke",
            "Pulmonary Arterial Hypertension",
            "Chronic obstructive pulmonary disease",
            "Asthma",
            "Breast cancer",
            "Colon and rectum cancer",
            "Cervical cancer",
            "Prostate cancer",
            "Cirrhosis and other chronic liver diseases",
            "Inflammatory bowel disease",
            "Alzheimer's disease and other dementias",
            "Parkinson's disease",
            "Alcohol use disorders",
            "Diabetes mellitus",
            "Chronic kidney disease",
            "Rheumatoid arthritis",
            "Maternal disorders",
            "Neonatal disorders",
            "Self-harm",
            "Interpersonal violence",
            "HIV/AIDS",
            "Tuberculosis",
            "Dengue",
            "Protein-energy malnutrition"
        ]
    year = 2021
    DEATH_DATA_PROCESSOR(year)
    M = UPDATE_RESULTS_FOR_OTHER_DISEASES()
    for disease in diseases:
        print(f"Calculating POPSTAT for {disease} disease")
        disease, country_correlations = POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, year).run()
        M.update_new_dataframe(disease, country_correlations)
    
    M.save_new_dataframe()
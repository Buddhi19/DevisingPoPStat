import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name
from ANALYSIS_FOR_OTHER_DISEASES.Death_data_Processor import DEATH_DATA_PROCESSOR
from ANALYSIS_FOR_OTHER_DISEASES.Pop_Stat_Calculation import POP_STAT_CALCULATION_FOR_OTHER_DISEASES
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE

death_data_path = os.path.join(main_dir, "DATA", "death_data", "DEATH_DATA.csv")
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

class MORTALITY_DATA:
    def __init__(self, year):
        self.year = year
        DEATH_DATA_PROCESSOR(year)
        POPULATION_DATA_FOR_DATE(year)
        self.DEATH_DATA = pd.read_csv(death_data_path, low_memory=False)
        self.CORR_COEFFICIENT = {
            "Parameter": [],
            "Cause of Death": [],
            "r squared value": [],
            "CI": [],
            "p-value": [],
            "reference_country": []
        }
        self.HDI_DATA = HDI_DATA[HDI_DATA['Year'] == int(self.year)]

        self.MEDIAN_AGE_DATA = MEDIAN_AGE_DATA[MEDIAN_AGE_DATA['Year'] == int(self.year)]
        self.MEDIAN_AGE_DATA.columns = ["Entity", "Code", "Year", "Median Age", ""]

        self.GDP_per_capita_data = GDP_PER_CAPITA_DATA[GDP_PER_CAPITA_DATA['Year'] == int(self.year)]
        self.Pop_Density = POPULATION_DENSITY[POPULATION_DENSITY['Year'] == int(self.year)]

        self.GINI_DATA = GINI_DATA[GINI_DATA['Year'] == int(self.year)]
        self.UHCI_DATA = UHCI_DATA[UHCI_DATA['Year'] == int(self.year)]
        self.LIFE_EXPECTANCY_DATA = LIFE_EXPECTANCY_DATA[LIFE_EXPECTANCY_DATA['Year'] == int(self.year)]

        if self.year <= 2019:
            self.SDI_data = SDI_DATA[["Location", str(self.year)]]

        self.data = self.DEATH_DATA
        self.deaths_per_disease: dict = {}

    def filter_death_data(self, disease):
        self.data = self.DEATH_DATA[self.DEATH_DATA['cause_name'] == disease]

    def create_death_data_per_disease(self, country):
        filtered_data = self.data
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
        reference_country_solver = POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, self.year)
        self.reference_country = reference_country_solver.run()
        POPSTAT = reference_country_solver.POPSTAT_DISEASE(self.reference_country) 
        data = self.data
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in POPSTAT.keys():
                continue
            popstat_val = POPSTAT[country]
            total_deaths_per_million = self.create_death_data_per_disease(pre_name)
            if not total_deaths_per_million:
                continue
            X.append(popstat_val)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, variable=f"POPSTAT_{disease}")

    def create_dataframe_for_diseases_SDI(self, disease):
        if self.year > 2019:
            return
        X = []
        Y = []
        data = self.data
        for country in data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in self.SDI_DATA['Location'].str.lower().values:
                continue
            SDI = self.SDI_DATA[self.SDI_DATA['Location'].str.lower() == country][str(self.year)].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(pre_name)
            if not total_deaths_per_million:
                continue
            X.append(SDI)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_SDI, variable = "SDI")

    def create_dataframe_for_diseases_and_plot(self, disease: str, variable_name: str, DATA: pd.DataFrame, saving_path, variable: str):
        """
        disease: disease we are analyzing
        variable_name: variable on the DATAFRAME 
        variable: variable name
        """
        X = []
        Y = []
        for country in self.data['location_name'].unique():
            pre_name = country
            country = mapping_name(country)
            if country == None:
                continue
            if country not in DATA['Entity'].str.lower().values:
                continue
            val = DATA[DATA['Entity'].str.lower() == country][variable_name].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(pre_name)
            if not total_deaths_per_million:
                continue
            X.append(val)
            Y.append(total_deaths_per_million)

        self.PLOT(X,Y, disease, saving_path=saving_path, variable = variable)

    def run(self, disease):
        self.filter_death_data(disease)
        self.create_dataframe_for_diseases(disease)
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Human Development Index",
            DATA = self.HDI_DATA,
            saving_path = SAVING_PATH_PNG_HDI,
            variable = "HDI"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Median Age",
            DATA = self.MEDIAN_AGE_DATA,
            saving_path = SAVING_PATH_PNG_MEDIAN_AGE,
            variable = "Median Age"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "GDP per capita",
            DATA = self.GDP_per_capita_data,
            saving_path = SAVING_PATH_PNG_GDP_PER_CAPITA,
            variable = "GDP per capita"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Population density",
            DATA = self.Pop_Density,
            saving_path = SAVING_PATH_PNG_POPULATION_DENSITY,
            variable = "Population Density"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Gini coefficient",
            DATA = self.GINI_DATA,
            saving_path = SAVING_PATH_PNG_GINI,
            variable = "Gini coefficient"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "UHC Service Coverage Index (SDG 3.8.1)",
            DATA = self.UHCI_DATA,
            saving_path = SAVING_PATH_PNG_UHCI,
            variable = "UHCI"
        )
        self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Period life expectancy at birth - Sex: all - Age: 0",
            DATA = self.LIFE_EXPECTANCY_DATA,
            saving_path = SAVING_PATH_PNG_LIFE_EXPECTANCY,
            variable = "Life expectancy"
        )


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
        self.CORR_COEFFICIENT['reference_country'].append(self.reference_country)

        z = np.polyfit(X, Y, 1)
        p = np.poly1d(z)
        plt.plot(X, p(X), "r--")

        plt.text(0.75, 0.95, f'R² = {r_squared:.3f}',
                        transform=plt.gca().transAxes, verticalalignment='top', fontsize = 'large')
        title = title.replace("/", "")
        plt.savefig(os.path.join(saving_path, f'{title}_deaths.png'))
        plt.close()

        print(f"Data for {title} has been plotted with {len(X)} countries for {variable}")
        print()

    def ANALYZER(self):
        causes = self.DEATH_DATA['cause_name'].unique()
        for disease in causes:
            self.run(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_custom.csv"))

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
            self.run(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_custom_selected.csv"))


if __name__ == "__main__":
    data = MORTALITY_DATA(2021)
    data.ANALYZER()
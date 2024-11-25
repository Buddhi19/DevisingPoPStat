import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name
from ANALYSIS.Plot_Population_Data import PLOT_POPULATION_DATA
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE
from ANALYSIS_FOR_OTHER_DISEASES.Death_data_Processor import DEATH_DATA_PROCESSOR, DEATH_DATA_PROCESSOR_FOR_SPAN
from ANALYSIS_FOR_OTHER_DISEASES.Pop_Stat_Calculation import POP_STAT_CALCULATION_FOR_OTHER_DISEASES
from ANALYSIS_FOR_OTHER_DISEASES.Plotter import PLOTTER

from ANALYSIS_FOR_OTHER_DISEASES.ALL_PATHS_DATA import *

class MORTALITY_DATA:
    def __init__(self, year, singleMode = True):
        self.singleMode = True if singleMode else False
        self.year = year
        DEATH_DATA_PROCESSOR(year) if singleMode else None
        POPULATION_DATA_FOR_DATE(year)
        self.DEATH_DATA = pd.read_csv(death_data_path if singleMode else death_data_path_for_span, low_memory=False)
        self.CORR_COEFFICIENT = {
            "Disease" : [],
            "PoPStat r" : [], 
            "PoPStat CI" : [], 
            "PoPStat p-value" : [], 
            "PoPStat reference country" : [], 
            "PoPStat r squared" : [], 

            "HDI r" : [], 
            "HDI CI" : [], 
            "HDI p-value" : [], 
            "HDI r squared" : [], 

            "SDI r" : [], 
            "SDI CI" : [], 
            "SDI p-value" : [], 
            "SDI r squared" : [], 

            "Median Age r" : [], 
            "Median Age CI" : [], 
            "Median Age p-value" : [], 
            "Median Age r squared" : [], 

            "GDP per capita r" : [], 
            "GDP per capita CI" : [], 
            "GDP per capita p-value" : [], 
            "GDP per capita r squared" : [], 

            "Population density r" : [], 
            "Population density CI" : [], 
            "Population density p-value" : [], 
            "Population density r squared" : [], 

            "Gini coefficient r" : [], 
            "Gini coefficient CI" : [], 
            "Gini coefficient p-value" : [], 
            "Gini coefficient r squared" : [], 

            "UHCI r" : [], 
            "UHCI CI" : [], 
            "UHCI p-value" : [], 
            "UHCI r squared" : [], 

            "Life expectancy r" : [], 
            "Life expectancy CI" : [], 
            "Life expectancy p-value" : [], 
            "Life expectancy r squared" : []
        }
        self.HDI_DATA = HDI_DATA[HDI_DATA['Year'] == int(self.year)]

        self.MEDIAN_AGE_DATA = MEDIAN_AGE_DATA[MEDIAN_AGE_DATA['Year'] == int(self.year)]
        self.MEDIAN_AGE_DATA.columns = ["Entity", "Code", "Year", "Median Age", ""]

        self.GDP_per_capita_data = GDP_PER_CAPITA_DATA[GDP_PER_CAPITA_DATA['Year'] == int(self.year)]
        self.Pop_Density = POPULATION_DENSITY[POPULATION_DENSITY['Year'] == int(self.year)]

        self.GINI_DATA = GINI_DATA[GINI_DATA['Year'] == int(self.year)]
        self.UHCI_DATA = UHCI_DATA[UHCI_DATA['Year'] == int(self.year)]
        self.LIFE_EXPECTANCY_DATA = LIFE_EXPECTANCY_DATA[LIFE_EXPECTANCY_DATA['Year'] == int(self.year)]

        self.SDI_DATA = SDI_DATA[["Location", str(self.year) if self.year < 2019 else "2019"]]

        self.data = self.DEATH_DATA
        self.deaths_per_disease: dict = {}

        self.DUMMY = {
            "correalation_coefficient": 0,
            "p_value": 0,
            "r_squared": 0,
            "CI": (0, 0)
        }

        self.ALL_PARAMETERS = [
            "PoPStat","HDI","SDI","Median Age","GDP per capita","Population density",
            "Gini coefficient","UHCI","Life expectancy"
        ]

    @classmethod
    def for_span(cls, start_year, end_year):
        cls.start_year = start_year
        cls.end_year = end_year
        DEATH_DATA_PROCESSOR_FOR_SPAN(start_year, end_year)
        POPULATION_DATA_FOR_DATE(end_year)
        return cls(start_year, singleMode = False)

    def filter_death_data(self, disease):
        self.data = self.DEATH_DATA[self.DEATH_DATA['cause_name'] == disease]

    def create_death_data_per_disease(self, country):
        filtered_data = self.data
        filtered_data = filtered_data[filtered_data['location_name'] == country]
        year_data = filtered_data
        if self.singleMode:
            year_data = filtered_data[filtered_data['year'] == self.year]
        else:
            year_data = filtered_data[filtered_data['year'] == f"{self.start_year}-{self.end_year}"]
        total_death_rate = year_data[year_data['metric_name'] == 'Rate']
        if total_death_rate.empty:
            return None
        total_deaths = total_death_rate['val'].values[0]
        return total_deaths
    
    def create_dataframe_for_diseases(self, disease,plot = True):
        X = []
        Y = []
        reference_country_solver = POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, self.year) if self.singleMode else POP_STAT_CALCULATION_FOR_OTHER_DISEASES(
            disease, f"{self.start_year}-{self.end_year}", singleMode = False)
        self.reference_country = reference_country_solver.run()
        POPSTAT = reference_country_solver.POPSTAT_DISEASE(self.reference_country)
        if not plot:
            POPSTAT_DATAFRAME = pd.DataFrame(POPSTAT.items(), columns = ["Country", "POPSTAT"])
            disease_name = disease.replace("/", "")
            POPSTAT_DATAFRAME.to_csv(
                os.path.join(FOR_UI_POPSTAT_PATH_FOR_YEAR(str(self.year)), f"{disease_name}_POPSTAT.csv") if self.singleMode else os.path.join(
                    FOR_UI_POPSTAT_PATH_FOR_YEAR(f"{self.start_year}_{self.end_year}"), f"{disease_name}_POPSTAT.csv"
                ), index = False
            )
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

        if plot:
            POPSTAT_REVERSE = {v:k for k,v in POPSTAT.items()} 
            Plotter = PLOTTER(POPSTAT, POPSTAT_REVERSE)
            if not Plotter.pre_process(X, Y):
                return {
                    "correalation_coefficient": 0,
                    "p_value": 0,
                    "r_squared": 0,
                    "CI": (0, 0),
                    "reference_country": "None"
                }
            data = Plotter.plot(disease, SAVING_PATH_PNG_FOR_YEAR(str(self.year)), "POPSTAT", disease) if self.singleMode else Plotter.plot(
                disease, SAVING_PATH_PNG_FOR_YEAR(f"{self.start_year}_{self.end_year}"), "POPSTAT", disease
            )
            data["reference_country"] = self.reference_country
            return data
        else:
            return X,Y

    def create_dataframe_for_diseases_SDI(self, disease, plot = True):
        SDI_YEAR = self.year
        if self.year > 2019:
            SDI_YEAR = 2019
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
            SDI = self.SDI_DATA[self.SDI_DATA['Location'].str.lower() == country][str(SDI_YEAR)].values[0]
            total_deaths_per_million = self.create_death_data_per_disease(pre_name)
            if not total_deaths_per_million:
                continue
            X.append(SDI)
            Y.append(total_deaths_per_million)

        if plot:
            return self.PLOT(X,Y, disease, saving_path=SAVING_PATH_PNG_SDI_FOR_YEAR(str(self.year)), variable = "SDI") if self.singleMode else self.PLOT(
                X,Y, disease, saving_path=SAVING_PATH_PNG_SDI_FOR_YEAR(f"{self.start_year}_{self.end_year}"), variable = "SDI"
            )
        else:
            return X,Y

    def create_dataframe_for_diseases_and_plot(self, disease: str, variable_name: str, DATA: pd.DataFrame, 
                                               saving_path, variable: str, plot = True):
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

        if plot:
            return self.PLOT(X,Y, disease, saving_path=saving_path, variable = variable)
        else:
            return X,Y

    def run(self, disease):
        self.filter_death_data(disease)
        POPSTAT_data = self.create_dataframe_for_diseases(disease)
        SDI_data = self.create_dataframe_for_diseases_SDI(disease)
        HDI_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Human Development Index",
            DATA = self.HDI_DATA,
            saving_path = SAVING_PATH_PNG_HDI_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_HDI_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "HDI"
        )
        MEDIAN_AGE_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Median Age",
            DATA = self.MEDIAN_AGE_DATA,
            saving_path = SAVING_PATH_PNG_MEDIAN_AGE_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_MEDIAN_AGE_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "Median Age"
        )
        GDP_PER_CAPITA_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "GDP per capita",
            DATA = self.GDP_per_capita_data,
            saving_path = SAVING_PATH_PNG_GDP_PER_CAPITA_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_GDP_PER_CAPITA_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "GDP per capita"
        )
        POPULATION_DENSITY_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Population density",
            DATA = self.Pop_Density,
            saving_path = SAVING_PATH_PNG_POPULATION_DENSITY_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_POPULATION_DENSITY_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "Population Density"
        )
        GINI_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Gini coefficient",
            DATA = self.GINI_DATA,
            saving_path = SAVING_PATH_PNG_GINI_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_GINI_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "Gini coefficient"
        )
        UHCI_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "UHC Service Coverage Index (SDG 3.8.1)",
            DATA = self.UHCI_DATA,
            saving_path = SAVING_PATH_PNG_UHCI_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_UHCI_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "UHCI"
        )
        LIFE_EXPECTANCY_data = self.create_dataframe_for_diseases_and_plot(
            disease = disease,
            variable_name = "Period life expectancy at birth - Sex: all - Age: 0",
            DATA = self.LIFE_EXPECTANCY_DATA,
            saving_path = SAVING_PATH_PNG_LIFE_EXPECTANCY_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_PNG_LIFE_EXPECTANCY_FOR_YEAR(f"{self.start_year}_{self.end_year}"),
            variable = "Life expectancy"
        )
        self.CORR_COEFFICIENT["Disease"].append(disease) 
        self.CORR_COEFFICIENT["PoPStat reference country"].append(POPSTAT_data["reference_country"])
        for data, key in zip(
            [POPSTAT_data, HDI_data, SDI_data, MEDIAN_AGE_data, GDP_PER_CAPITA_data, POPULATION_DENSITY_data, GINI_data, UHCI_data, LIFE_EXPECTANCY_data],
            self.ALL_PARAMETERS
        ):
            self.CORR_COEFFICIENT[f"{key} r"].append(data["correalation_coefficient"])
            self.CORR_COEFFICIENT[f"{key} CI"].append(data["CI"])
            self.CORR_COEFFICIENT[f"{key} p-value"].append(data["p_value"])
            self.CORR_COEFFICIENT[f"{key} r squared"].append(data["r_squared"])



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
            return self.DUMMY
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
        return {
            "correalation_coefficient": correalation_coefficient,
            "p_value": p_value,
            "r_squared": r_squared,
            "CI": (lo, hi)
        }

    def ANALYZER(self):
        causes = self.DEATH_DATA['cause_name'].unique()
        for disease in causes:
            self.run(disease)
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        SAVING_PATH_CSV = SAVING_PATH_CSV_FOR_YEAR(str(self.year)) if self.singleMode else SAVING_PATH_CSV_FOR_YEAR(f"{self.start_year}_{self.end_year}")
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_custom.csv"))

    def ANALYZER_FOR_SELECTED_DISEASES(self):
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
            "Liver cancer",
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
        for disease in diseases:
            self.run(disease)
        # remove other metrics columns
        self.CORR_COEFFICIENT = {
            v: self.CORR_COEFFICIENT[v] for v in self.CORR_COEFFICIENT if v in ["Disease", "PoPStat r", "PoPStat CI", "PoPStat p-value", "PoPStat reference country", "PoPStat r squared"]
        }
        self.CORR_COEFFICIENT = pd.DataFrame(self.CORR_COEFFICIENT)
        self.CORR_COEFFICIENT.to_csv(os.path.join(SAVING_PATH_CSV, f"Correlation_Coefficient_selected.csv"), index = False)

    def save_plot_data(self):
        for disease in self.DEATH_DATA['cause_name'].unique():
            self.filter_death_data(disease)
            X, Y = self.create_dataframe_for_diseases(disease, plot = False)
            data = pd.DataFrame({"X": X, "Y": Y})
            disease_name = disease.replace("/", " ")
            saving_path_XY = os.path.join(
                FOR_UI_PATH_FOR_YEAR(str(self.year)), f"{disease_name}_POPSTAT.csv"
            ) if self.singleMode else os.path.join(
                FOR_UI_PATH_FOR_YEAR(f"{self.start_year}_{self.end_year}"), f"{disease_name}_POPSTAT.csv")
            data.to_csv(saving_path_XY, index = False)
            X, Y = self.create_dataframe_for_diseases_SDI(disease, plot = False)
            data = pd.DataFrame({"X": X, "Y": Y})
            saving_path_XY = os.path.join(
                FOR_UI_PATH_FOR_YEAR(str(self.year)), f"{disease_name}_SDI.csv"
            ) if self.singleMode else os.path.join(
                FOR_UI_PATH_FOR_YEAR(f"{self.start_year}_{self.end_year}"), f"{disease_name}_SDI.csv")
            data.to_csv(saving_path_XY, index = False)

            for variable_name, DATA, variable in zip(
                [
                    "Human Development Index",
                    "Median Age",
                    "GDP per capita",
                    "Population density",
                    "Gini coefficient",
                    "UHC Service Coverage Index (SDG 3.8.1)",
                    "Period life expectancy at birth - Sex: all - Age: 0"
                ],
                [
                    self.HDI_DATA,
                    self.MEDIAN_AGE_DATA,
                    self.GDP_per_capita_data,
                    self.Pop_Density,
                    self.GINI_DATA,
                    self.UHCI_DATA,
                    self.LIFE_EXPECTANCY_DATA
                ],
                [
                    "HDI",
                    "Median Age",
                    "GDP per capita",
                    "Population Density",
                    "Gini coefficient",
                    "UHCI",
                    "Life expectancy"
                ]
            ):
                X, Y = self.create_dataframe_for_diseases_and_plot(
                    disease = disease,
                    variable_name = variable_name,
                    DATA = DATA,
                    saving_path = None,
                    variable = variable,
                    plot = False
                )
                data = pd.DataFrame({"X": X, "Y": Y})
                saving_path_XY = os.path.join(
                    FOR_UI_PATH_FOR_YEAR(str(self.year)), f"{disease_name}_{variable}.csv"
                ) if self.singleMode else os.path.join(
                    FOR_UI_PATH_FOR_YEAR(f"{self.start_year}_{self.end_year}"), f"{disease_name}_{variable}.csv")
                data.to_csv(saving_path_XY, index = False)

        pyramids = PLOT_POPULATION_DATA()
        pyramids.generate_all_pyramids(FOR_UI_PYRAMIDS_PATH_FOR_YEAR(str(self.year)) if self.singleMode else FOR_UI_PYRAMIDS_PATH_FOR_YEAR(f"{self.start_year}_{self.end_year}"))


if __name__ == "__main__":
    M = MORTALITY_DATA(2021)
    M.ANALYZER_FOR_SELECTED_DISEASES()
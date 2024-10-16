import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.Covid_Data_For_Date import COVID_DATA_FOR_DATE
from ANALYSIS.Plot_Population_Data import PLOT_POPULATION_DATA
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Plot_Pop_Stat import PLOT_POP_STAT
from ANALYSIS.Process_Owid_Data import process_country_names
from ANALYSIS.Plot_other_Metrics import PLOT_OTHER_METRICS
from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE

SAVING_DIR = os.path.join(main_dir, "RESULTS/POPSTATCOVID")

class ANALYSIS:
    def __init__(self):
        self.common_countries = []
        self.year = '2020'
        self.POPSTAT_DATAFRAME = {
            "Reference Country/ Metric": [],
            "r_squared_cases": [],
            "CI_cases": [],
            "p_value_cases": [],
            "r_squared_deaths": [],
            "CI_deaths": [],
            "p_value_deaths": []
        }

    def create_country_population_data(self):
        date = input("Date in YYYY or Press Enter to set year as 2020 : ")
        if date == "":
            date = '2020'
        self.year = date
        POPULATION_DATA_FOR_DATE(date)

    @staticmethod
    def create_country_covid_data():
        DATE_AS_PER_PAPER = '2023-05-05'
        date = input(f"Date in YYYY-MM-DD or Press Enter to set date as {DATE_AS_PER_PAPER} : ")
        if date == "":
            date = DATE_AS_PER_PAPER
        COVID_DATA_FOR_DATE(date)

    @staticmethod
    def plot_population_data():
        plotter = PLOT_POPULATION_DATA()
        plotter.run()

    @staticmethod
    def prepare_data():
        process_country_names()

    def plot_other_metrics(self):
        plotter = PLOT_OTHER_METRICS(self.common_countries, self.year)
        Stats = plotter.MEDIAN_AGE()
        self.update_POPSTAT_DATAFRAME(Stats, "Median Age")

        Stats = plotter.GDP_PER_CAPITA() if int(self.year) <= 2022 else None
        self.update_POPSTAT_DATAFRAME(Stats, "GDP Per Capita") if Stats is not None else None

        Stats = plotter.POPULATION_DENSITY()
        self.update_POPSTAT_DATAFRAME(Stats, "Population Density")

        Stats = plotter.HUMAN_DEVELOPMENT_INDEX()
        self.update_POPSTAT_DATAFRAME(Stats, "Human Development Index")

        Stats = plotter.LIFE_EXPECTANCY() if int(self.year) <= 2021 else None
        self.update_POPSTAT_DATAFRAME(Stats, "Life Expectancy") if Stats is not None else None

        Stats = plotter.SDI()
        self.update_POPSTAT_DATAFRAME(Stats, "SDI") if Stats is not None else None

        Stats = plotter.GNI() if int(self.year) <= 2021 else None
        self.update_POPSTAT_DATAFRAME(Stats, "GNI") if Stats is not None else None

        Stats = plotter.UNIVERSAL_HEALTH_COVERAGE() if int(self.year) <= 2021 else None
        self.update_POPSTAT_DATAFRAME(Stats, "Universal Health Coverage") if Stats is not None else None

        Stats = plotter.GNI_INDEX()
        self.update_POPSTAT_DATAFRAME(Stats, "GNI Index")

    def calculate_pop_stat(self):
        calculator = POP_STAT_CALCULATION()
        self.progressive_reference_countries, self.regressive_reference_countries = calculator.run()
        self.common_countries = calculator.common_countries

    
    def update_POPSTAT_DATAFRAME(self, Stats, parameter):
        self.POPSTAT_DATAFRAME["Reference Country/ Metric"].append(parameter)

        self.POPSTAT_DATAFRAME["r_squared_cases"].append(Stats["cases"][0])
        self.POPSTAT_DATAFRAME["CI_cases"].append(Stats["cases"][1])
        self.POPSTAT_DATAFRAME["p_value_cases"].append(Stats["cases"][2])

        self.POPSTAT_DATAFRAME["r_squared_deaths"].append(Stats["deaths"][0])
        self.POPSTAT_DATAFRAME["CI_deaths"].append(Stats["deaths"][1])
        self.POPSTAT_DATAFRAME["p_value_deaths"].append(Stats["deaths"][2])

    def plot_pop_stat(self):
        for country, _ in self.progressive_reference_countries:
            plotter = PLOT_POP_STAT(country, True)
            Stats = plotter.run()
            self.update_POPSTAT_DATAFRAME(Stats, country)
            
        for country, _ in self.regressive_reference_countries:
            plotter = PLOT_POP_STAT(country, False)
            Stats = plotter.run()
            self.update_POPSTAT_DATAFRAME(Stats, country)


    def run(self):
        self.create_country_population_data()
        self.create_country_covid_data()
        self.plot_population_data()
        self.calculate_pop_stat()
        self.plot_pop_stat()
        self.prepare_data()
        self.plot_other_metrics()

        pd.DataFrame(self.POPSTAT_DATAFRAME).to_csv(os.path.join(SAVING_DIR, f'POPSTAT_COVID19_KL_DIVERGENCE.csv'), index = False)

    def parser_run(self, pop_year=2020, covid_date='2023-05-05', plotter=True):
        POPULATION_DATA_FOR_DATE(pop_year)
        COVID_DATA_FOR_DATE(covid_date)
        if plotter:
            self.plot_population_data()
        self.calculate_pop_stat()
        self.plot_pop_stat()
        self.prepare_data()
        self.plot_other_metrics()

        pd.DataFrame(self.POPSTAT_DATAFRAME).to_csv(os.path.join(SAVING_DIR, f'POPSTAT_COVID19_KL_DIVERGENCE.csv'), index = False)

if __name__ == "__main__":
        ANALYSIS().run()
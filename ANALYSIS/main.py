import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.Covid_Data_For_Date import COVID_DATA_FOR_DATE
from ANALYSIS.Plot_Population_Data import PLOT_POPULATION_DATA
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Plot_Pop_Stat import PLOT_POP_STAT
from ANALYSIS.Plot_other_Metrics import PLOT_OTHER_METRICS
from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE

class ANALYSIS:
    def __init__(self):
        self.common_countries = []
        self.year = '2020'

    def create_country_population_data(self):
        date = input("Date in YYYY or Press Enter to set year as 2020 : ")
        if date == "":
            date = '2020'
        self.year = date
        POPULATION_DATA_FOR_DATE(date)

    @staticmethod
    def create_country_covid_data():
        DATE_AS_PER_PAPER = '2022-04-08'
        date = input(f"Date in YYYY-MM-DD or Press Enter to set date as {DATE_AS_PER_PAPER} : ")
        if date == "":
            date = DATE_AS_PER_PAPER
        COVID_DATA_FOR_DATE(date)

    @staticmethod
    def plot_population_data():
        plotter = PLOT_POPULATION_DATA()
        plotter.run()

    def plot_other_metrics(self):
        plotter = PLOT_OTHER_METRICS(self.common_countries, self.year)
        plotter.MEDIAN_AGE()
        plotter.GDP_PER_CAPITA()
        plotter.POPULATION_DENSITY()
        plotter.HUMAN_DEVELOPMENT_INDEX()
        plotter.LIFE_EXPECTANCY()

    def calculate_pop_stat(self):
        calculator = POP_STAT_CALCULATION()
        self.progressive_reference_countries, self.regressive_reference_countries = calculator.run()
        self.common_countries = calculator.common_countries

    def plot_pop_stat(self):
        for country, _ in self.progressive_reference_countries:
            plotter = PLOT_POP_STAT(country, True)
            plotter.run()

        for country, _ in self.regressive_reference_countries:
            plotter = PLOT_POP_STAT(country, False)
            plotter.run()

    def run(self):
        self.create_country_population_data()
        self.create_country_covid_data()
        self.plot_population_data()
        self.calculate_pop_stat()
        self.plot_pop_stat()
        self.plot_other_metrics()

    def parser_run(self, pop_year, covid_date):
        POPULATION_DATA_FOR_DATE(pop_year)
        COVID_DATA_FOR_DATE(covid_date)
        self.plot_population_data()
        self.calculate_pop_stat()
        self.plot_pop_stat()
        self.plot_other_metrics()

if __name__ == "__main__":
        ANALYSIS().run()
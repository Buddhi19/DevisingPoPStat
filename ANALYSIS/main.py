import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from Covid_Data_For_Date import COVID_DATA_FOR_DATE
from Plot_Population_Data import PLOT_POPULATION_DATA
from Pop_Stat_Calculation import POP_STAT_CALCULATION
from Plot_Pop_Stat import PLOT_POP_STAT
from Plot_other_Metrics import PLOT_OTHER_METRICS

COUNTRY_DATA_PATH = os.path.join(main_dir, 'Data\\countries\\country_names.csv')

class ANALYSIS:
    def __init__(self):
        self.REFERENCE_COUNTRY = 'japan'
    def construct_countries(self):
        data = pd.read_csv(COUNTRY_DATA_PATH).iloc[:, 0]
        countries = []
        for country in data:
            if not country:
                continue
            countries.append(country.lower())

        with open(os.path.join(main_dir, 'ANALYSIS\\COUNTRIES.py'), 'w') as f:
            f.write(f'COUNTRIES = {countries}')

    def create_country_data(self):
        DATE_AS_PER_PAPER = '2022-04-08'
        date = input(f"Date in YYYY-MM-DD or Press Enter to set date as {DATE_AS_PER_PAPER} : ")
        if date == "":
            date = DATE_AS_PER_PAPER
        COVID_DATA_FOR_DATE(date)

    def plot_population_data(self):
        plotter = PLOT_POPULATION_DATA()
        plotter.run()

    def calculate_pop_stat(self):
        calculator = POP_STAT_CALCULATION()
        self.REFERENCE_COUNTRY = calculator.run()

    def plot_pop_stat(self):
        plotter = PLOT_POP_STAT(self.REFERENCE_COUNTRY)
        plotter.run()

    def plot_other_metrics(self):
        plotter = PLOT_OTHER_METRICS()
        plotter.MEDIAN_AGE()
        plotter.GDP_PER_CAPITA()
        plotter.POPULATION_DENSITY()

    def run(self):
        self.construct_countries()
        self.create_country_data()
        self.plot_population_data()
        self.calculate_pop_stat()
        self.plot_pop_stat()
        self.plot_other_metrics()

if __name__ == "__main__":
        ANALYSIS().run()
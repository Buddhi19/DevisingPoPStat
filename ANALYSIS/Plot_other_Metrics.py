import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np
from scipy import stats

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

COVID_DATA_DIR = os.path.join(main_dir, 'Data/covid_data_by_country')
SAVE_DIR = os.path.join(main_dir, 'RESULTS/POPSTATCOVID/OTHER_METRICS')
MEDIAN_AGE_DATA = os.path.join(main_dir, 'Data/owid_data/median-age.csv')
GDP_PER_CAPITA_DATA = os.path.join(main_dir, 'Data/owid_data/gdp-per-capita.csv')
POPULATION_DENSITY_DATA = os.path.join(main_dir, 'Data/owid_data/population-density.csv')
HUMAN_DEVELOPMENT_INDEX_DATA = os.path.join(main_dir, 'Data/owid_data/human-development-index.csv')
LIFE_EXPECTANCY_DATA = os.path.join(main_dir, 'Data/owid_data/life-expectancy.csv')

class PLOT_OTHER_METRICS:
    def __init__(self, countries, year):
        self.year = year
        self.countries = countries
        self.Y_CASES = []
        self.Y_DEATHS = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            self.Y_DEATHS.append(np.log(data['total_deaths_per_million'].values[0]))
            self.Y_CASES.append(np.log(data['total_cases_per_million'].values[0]))

        self.Median_age_data = pd.read_csv(MEDIAN_AGE_DATA)
        self.Median_age_data = self.Median_age_data[self.Median_age_data['Year'] == int(self.year)]
        self.Median_age_data.columns = ['Entity', 'Code', 'Year', 'Median age', '']

        self.GDP_per_capita_data = pd.read_csv(GDP_PER_CAPITA_DATA)
        self.GDP_per_capita_data = self.GDP_per_capita_data[self.GDP_per_capita_data['Year'] == int(self.year)]
        self.GDP_per_capita_data.columns = ['Entity', 'Code', 'Year', 'GDP per capita','']

        self.Population_density_data = pd.read_csv(POPULATION_DENSITY_DATA)
        self.Population_density_data = self.Population_density_data[self.Population_density_data['Year'] == int(self.year)]

        self.Human_development_index_data = pd.read_csv(HUMAN_DEVELOPMENT_INDEX_DATA)
        self.Human_development_index_data = self.Human_development_index_data[self.Human_development_index_data['Year'] == int(self.year)]

        self.Life_expectancy_data = pd.read_csv(LIFE_EXPECTANCY_DATA)
        self.Life_expectancy_data = self.Life_expectancy_data[self.Life_expectancy_data['Year'] == int(self.year)]
        self.Life_expectancy_data.columns = ['Entity', 'Code', 'Year', 'Life expectancy']

        
    def MEDIAN_AGE(self):
        X = []
        for country in self.countries:
            data = self.Median_age_data[self.Median_age_data['Entity'].str.lower() == country]
            X.append(data['Median age'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Median Age (years)")
        self.plotter(X,self.Y_DEATHS,"Deaths","Median Age (years)")

    def GDP_PER_CAPITA(self):
        X = []
        Y_CASES_filtered = []
        Y_DEATHS_filtered = []
        i = 0
        for country in self.countries:
            data = self.GDP_per_capita_data[self.GDP_per_capita_data['Entity'].str.lower() == country]
            if data.empty:
                i += 1
                continue
            X.append(data['GDP per capita'].values[0])
            Y_CASES_filtered.append(self.Y_CASES[i])
            Y_DEATHS_filtered.append(self.Y_DEATHS[i])
            i += 1

        self.plotter(X,Y_CASES_filtered,"Cases","GDP per Capita (USD)")
        self.plotter(X,Y_DEATHS_filtered,"Deaths","GDP per Capita (USD)")

    def POPULATION_DENSITY(self):
        X = []
        for country in self.countries:
            data = self.Population_density_data[self.Population_density_data['Entity'].str.lower() == country]
            X.append(data['Population density'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Population Density (per km²)")
        self.plotter(X,self.Y_DEATHS,"Deaths","Population Density (per km²)")

    def HUMAN_DEVELOPMENT_INDEX(self):
        X = []
        Y_CASES_filtered = []
        Y_DEATHS_filtered = []
        i = 0
        for country in self.countries:
            data = self.Human_development_index_data[self.Human_development_index_data['Entity'].str.lower() == country]
            if data.empty:
                i += 1
                continue
            X.append(data['Human Development Index'].values[0])
            Y_CASES_filtered.append(self.Y_CASES[i])
            Y_DEATHS_filtered.append(self.Y_DEATHS[i])
            i += 1

        self.plotter(X,Y_CASES_filtered,"Cases","Human Development Index")
        self.plotter(X,Y_DEATHS_filtered,"Deaths","Human Development Index")

    def LIFE_EXPECTANCY(self):
        X = []
        Y_CASES_filtered = []
        Y_DEATHS_filtered = []
        i = 0
        for country in self.countries:
            data = self.Life_expectancy_data[self.Life_expectancy_data['Entity'].str.lower() == country]
            if data.empty:
                i += 1
                continue
            X.append(data['Life expectancy'].values[0])
            Y_CASES_filtered.append(self.Y_CASES[i])
            Y_DEATHS_filtered.append(self.Y_DEATHS[i])
            i += 1

        self.plotter(X,Y_CASES_filtered,"Cases","Life Expectancy")
        self.plotter(X,Y_DEATHS_filtered,"Deaths","Life Expectancy")

    def plotter(self,X,Y,title,metric,save_dir=SAVE_DIR):
        plt.figure(figsize=(10, 6))
        plt.scatter(X, Y)
        plt.xlabel(metric)
        plt.ylabel(f"COVID19 {title} per million (log)")

        #remove nan values pairs
        X = np.array(X)
        Y = np.array(Y)
        mask = ~np.isnan(X) & ~np.isnan(Y)
        X = X[mask]
        Y = Y[mask]

        z = np.polyfit(X, Y, 1)
        p = np.poly1d(z)
        # plt.plot(X, p(X), "r",)
        # calculate the R² and confidence interval
        correlation_coefficient = np.corrcoef(X,Y)[0,1]
        r_squared = correlation_coefficient ** 2
        n = len(X)
        r_z = np.arctanh(correlation_coefficient)
        se = 1/np.sqrt(n-3)
        z = stats.norm.ppf((1+0.95)/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))
        print(f"R² = {r_squared:.3f} for {title}")
        print(f"95% confidence interval: {lo:.3f} to {hi:.3f} for {title}")

        plt.plot(X, p(X), "r-",label = f"R² = {r_squared:.5f}")

        plt.text(0.05, 0.95, f'R² = {r_squared:.5f}',
                     transform=plt.gca().transAxes, verticalalignment='top')

        plt.savefig(os.path.join(save_dir, f'Total_{title}_per_million_for_{metric}.png'))
        plt.close()
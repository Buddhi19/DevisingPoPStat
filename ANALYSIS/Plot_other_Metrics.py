import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np
from scipy import stats

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

COVID_DATA_DIR = os.path.join(main_dir, 'Data\\covid_data_by_country')
SAVE_DIR = os.path.join(main_dir, 'RESULTS\\POPSTATCOVID\\OTHER_METRICS')

class PLOT_OTHER_METRICS:
    def __init__(self, countries):
        self.countries = countries
        self.Y_CASES = []
        self.Y_DEATHS = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            self.Y_DEATHS.append(np.log(data['total_deaths_per_million'].values[0]))
            self.Y_CASES.append(np.log(data['total_cases_per_million'].values[0]))
        
    def MEDIAN_AGE(self):
        X = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            X.append(data['median_age'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Median Age (years)")
        self.plotter(X,self.Y_DEATHS,"Deaths","Median Age (years)")

    def GDP_PER_CAPITA(self):
        X = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            X.append(data['gdp_per_capita'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","GDP per Capita (USD)")
        self.plotter(X,self.Y_DEATHS,"Deaths","GDP per Capita (USD)")

    def POPULATION_DENSITY(self):
        X = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            X.append(data['population_density'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Population Density (per km²)")
        self.plotter(X,self.Y_DEATHS,"Deaths","Population Density (per km²)")

    def HUMAN_DEVELOPMENT_INDEX(self):
        X = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            X.append(data['human_development_index'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Human Development Index")
        self.plotter(X,self.Y_DEATHS,"Deaths","Human Development Index")

    def LIFE_EXPECTANCY(self):
        X = []
        for country in self.countries:
            data = pd.read_csv(os.path.join(COVID_DATA_DIR, f'{country}_covid_data.csv'))
            X.append(data['life_expectancy'].values[0])

        self.plotter(X,self.Y_CASES,"Cases","Life Expectancy")
        self.plotter(X,self.Y_DEATHS,"Deaths","Life Expectancy")

    def plotter(self,X,Y,title,metric):
        plt.figure(figsize=(10, 6))
        Y = None
        if title == "Cases":
            Y = self.Y_CASES
        elif title == "Deaths":
            Y = self.Y_DEATHS
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

        plt.savefig(os.path.join(SAVE_DIR, f'Total_{title}_per_million_for_{metric}.png'))
        plt.close()
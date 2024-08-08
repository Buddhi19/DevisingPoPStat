import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

COVID_DIR = os.path.join(main_dir, 'Data/covid_data_by_country')
POP_STAT_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_COUNTRY_DATA')
SAVE_DIR_PROGRESSIVE = os.path.join(main_dir, 'RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE')
SAVE_DIR_REGRESSIVE = os.path.join(main_dir, 'RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE')


class PLOT_POP_STAT:
    def __init__(self,country,progressive:bool):
        self.SAVE_DIR = SAVE_DIR_PROGRESSIVE if progressive else SAVE_DIR_REGRESSIVE
        self.country = country
        self.POP_STAT_DATA = pd.read_csv(os.path.join(POP_STAT_DIR, f'{self.country}_POPSTAT_COVID19.csv'))

    def POP_STAT_PLOT(self,title):
        X = []
        Y = []
        for country in self.POP_STAT_DATA["Country"]:
            x = self.POP_STAT_DATA[self.POP_STAT_DATA["Country"] == country]["POPSTAT_COVID19"].values[0]
            X.append(x)
            covid_data = pd.read_csv(os.path.join(COVID_DIR, f'{country}_covid_data.csv'))
            Y.append(np.log(covid_data[f"total_{title}_per_million"].values[0]))
            
        correlation_coefficient, p_value = stats.pearsonr(X, Y)
        r_squared = correlation_coefficient ** 2

        n = len(X)
        r_z = np.arctanh(correlation_coefficient)
        se = 1/np.sqrt(n-3)
        z = stats.norm.ppf((1+0.95)/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))

        print(f"R² = {r_squared:.3f} for {title}")
        print(f"Correlation coefficient = {correlation_coefficient:.3f} for {title}")
        print(f"95% confidence interval: {lo:.3f} to {hi:.3f} for {title}")
        print(f"p-value = {p_value:.6f} for {title}")

        self.plotter(X,Y,r_squared,title)
    
    def plotter(self,X,Y,r_squared,title):
        plt.figure(figsize=(10, 6))
        plt.scatter(X, Y)
        plt.xlabel("POPSTAT_COVID19")
        plt.ylabel(f"COVID19 {title} per million (log)")

        z = np.polyfit(X, Y, 1)
        p = np.poly1d(z)
        plt.plot(X, p(X), "r--")

        plt.text(0.05, 0.95, f'R² = {r_squared:.3f}',
                     transform=plt.gca().transAxes, verticalalignment='top')
        plt.title(f"Reference Country: {self.country}")
        plt.savefig(os.path.join(self.SAVE_DIR, f'{title}/Total_{title}_per_million_with_reference_{self.country}.png'))
        plt.close()

    def run(self):
        self.POP_STAT_PLOT("cases")
        self.POP_STAT_PLOT("deaths")
        print("Plots saved successfully")



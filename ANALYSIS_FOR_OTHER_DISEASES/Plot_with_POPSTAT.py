import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

death_data = pd.read_csv("DATA/deaths_by_cause_per_country/analyse_data.csv")

reference_country = "japan"
POPSTAT_DATA = pd.read_csv(f"Results/POPSTAT_COUNTRY_DATA/{reference_country}_POPSTAT_COVID19.csv")

X = []
Y = []

for row in death_data.itertuples():
    if not row:
        continue
    country = row[1]
    if country in POPSTAT_DATA["Country"].values:
        X.append(POPSTAT_DATA[POPSTAT_DATA["Country"] == country]["POPSTAT_COVID19"].iloc[0])
        Y.append(np.log(row[7]))
    print(country)

plt.scatter(X, Y)
plt.xlabel("POPSTAT_COVID19")
plt.ylabel("Meningitis Deaths/Log")

#add correlation line and R² value
r_squared = stats.pearsonr(X, Y)[0] ** 2
m, b = np.polyfit(X, Y, 1)

plt.plot(X, m * np.array(X) + b, "r--")

plt.text(0.05, 0.95, f'R² = {r_squared:.3f}',
                     transform=plt.gca().transAxes, verticalalignment='top')

plt.show()
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import pearsonr
from scipy import stats

class PLOTTER:
    def __init__(self, POPSTAT,POPSTAT_REVERSE):
        self.X = None
        self.Y = None
        self.POPSTAT = POPSTAT
        self.POPSTAT_REVERSE = POPSTAT_REVERSE
        self.dark_colors = [
            "#ef4444",  # Coral Red
            "#10b981",  # Emerald Green
            "#8b5cf6",  # Royal Purple
            "#f97316",  # Sunset Orange
            "#e11d48",  # Rose Red
            "#22c55e",  # Spring Green
            "#a855f7",  # Orchid Purple
            "#ea580c",  # Burnt Orange
            "#059669",  # Forest Green
            "#db2777",  # Deep Pink
            "#7c3aed",  # Electric Purple
            "#d97706",  # Amber
            "#dc2626",  # Ruby Red
            "#15803d",  # Hunter Green
            "#e879f9",  # Bright Pink
            "#92400e",  # Terracotta
            "#be185d",  # Raspberry
            "#16a34a",  # Garden Green
            "#9333ea",  # Amethyst Purple
            "#854d0e",  # Rich Bronze
            "#f43f5e",  # Strawberry
            "#a16207",  # Antique Gold
            "#ec4899",  # Magenta Pink
            "#b45309"   # Bronze
        ]

    def pre_process(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        MASK = (Y > 0)
        Y = Y[MASK]
        X = X[MASK]
        Y = np.log(Y)
        if len(X) < 2 or len(Y) < 2:
            return False
        self.X = X
        self.Y = Y
        return True


    def select_countries(self):
        """
        select 20 countries that are closer to the line of best fit 
        over the span of X
        """
        m, b = np.polyfit(self.X, self.Y, 1)
        dist = np.abs(self.Y - (m * self.X + b))
        
        idx_data = {
            self.X[i]: dist[i] for i in range(len(self.X))
        }

        range_0to25 = np.percentile(self.X, 25)
        range_0to50 = np.percentile(self.X, 50)
        range_0to75 = np.percentile(self.X, 75)
        range_0to85 = np.percentile(self.X, 85)

        idx1_data = {
            key: value for key, value in idx_data.items() if key < range_0to25
        }
        idx2_data = {
            key: value for key, value in idx_data.items() if range_0to25 <= key < range_0to50
        }
        idx3_data = {
            key: value for key, value in idx_data.items() if range_0to50 <= key < range_0to75
        }
        idx4_data = {
            key: value for key, value in idx_data.items() if range_0to75 <= key < range_0to85
        }
        idx5_data = {
            key: value for key, value in idx_data.items() if range_0to85 <= key
        }

        idx1_data = sorted(idx1_data.items(), key=lambda x: x[1])
        idx2_data = sorted(idx2_data.items(), key=lambda x: x[1])
        idx3_data = sorted(idx3_data.items(), key=lambda x: x[1])
        idx4_data = sorted(idx4_data.items(), key=lambda x: x[1])
        idx5_data = sorted(idx5_data.items(), key=lambda x: x[1])

        idx1 = [
            idx1_data[i][0] for i in range(min(len(idx1_data),3))
        ]
        idx2 = [
            idx2_data[i][0] for i in range(min(len(idx2_data),5))
        ]
        idx3 = [
            idx3_data[i][0] for i in range(min(len(idx3_data),5))
        ]
        idx4 = [
            idx4_data[i][0] for i in range(min(len(idx4_data),4))
        ]
        idx5 = [
            idx5_data[i][0] for i in range(min(len(idx5_data),4))
        ]
        
        idx1_indexes = np.where(np.isin(self.X, idx1))[0]
        idx2_indexes = np.where(np.isin(self.X, idx2))[0]
        idx3_indexes = np.where(np.isin(self.X, idx3))[0]
        idx4_indexes = np.where(np.isin(self.X, idx4))[0]
        idx5_indexes = np.where(np.isin(self.X, idx5))[0]

        return idx1_indexes, idx2_indexes, idx3_indexes, idx4_indexes, idx5_indexes
    
    def country_name_formatter(self, country):
        # capitalize the first letter of each word
        country = " ".join([word.capitalize() for word in country.split()])
        return country

    def plot(self,title, saving_path, variable,disease):
        plt.figure(figsize=(10, 6))
        m, b = np.polyfit(self.X, self.Y, 1)

        idx1, idx2, idx3, idx4, idx5 = self.select_countries()

        color_index = 0
        plt.plot(self.X, (m * self.X + b), color='red', linewidth=1)
        idx1, idx2, idx3, idx4, idx5 = list(idx1), list(idx2), list(idx3), list(idx4), list(idx5)
        
        called = idx1 + idx2 + idx3 + idx4
        other_X = [
            self.X[i] for i in range(len(self.X)) if i not in called
        ]
        other_Y = [
            self.Y[i] for i in range(len(self.Y)) if i not in called
        ]
        plt.scatter(
            other_X, other_Y, color = "blue"
        )

        for idx, _ in zip([idx1, idx2, idx3, idx4, idx5], self.dark_colors):
            for i in idx:
                plt.scatter(
                    self.X[i], self.Y[i], color=self.dark_colors[color_index],
                    s = 80, label=self.country_name_formatter(self.POPSTAT_REVERSE[self.X[i]])
                )
                color_index += 1

        correalation_coefficient, p_value = pearsonr(self.X, self.Y)
        r_squared = correalation_coefficient ** 2

        n = len(self.X)
        r_z = np.arctanh(correalation_coefficient)
        se = 1/np.sqrt(n-3)
        z = stats.norm.ppf((1+0.95)/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))

        plt.xlabel(f'{variable} {disease}')
        plt.ylabel('Natural Log of Deaths per Million')
        plt.title(title)
        plt.legend(frameon=False, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        disease_name = disease.replace("/", " ")
        plt.savefig(
            os.path.join(saving_path, f'{disease_name}_deaths.png')
        )
        plt.close()
        return {
            "correalation_coefficient": correalation_coefficient,
            "p_value": p_value,
            "r_squared": r_squared,
            "CI": (lo, hi)
        }

    def custom_plotter(self,title, saving_path, variable,disease):
        
        self.countries = [
            "congo",
            "benin",
            "sierra leone",
            "pakistan",
            "samoa",
            "jordan",
            "belize",
            "belize",
            "el salvador",
            "kazakhstan",
            "tunisia",
            "sri lanka",
            "bahamas",
            "moldova",
            "united states",
            "sweden",
            "france",
            "finland",
            "italy"
        ]
        values_filtered = [
            self.POPSTAT[country] for country in self.countries
        ]
        idx_values_filtered = list(np.where(np.isin(self.X, values_filtered))[0])

        other_X = [
            self.X[i] for i in range(len(self.X)) if i not in idx_values_filtered
        ]
        other_Y = [
            self.Y[i] for i in range(len(self.Y)) if i not in idx_values_filtered
        ]

        plt.figure(figsize=(10, 6))
        m, b = np.polyfit(self.X, self.Y, 1)
        plt.plot(self.X, (m * self.X + b), color='red', linewidth=1)
        plt.scatter(
            other_X, other_Y, color = "blue"
        )

        color_index = 0
        for country in self.countries:
            idx = self.POPSTAT[country]
            idx = np.where(self.X == idx)[0][0]
            plt.scatter(
                self.X[idx], self.Y[idx], color=self.dark_colors[color_index],
                s = 80, label=self.country_name_formatter(country)
            )
            color_index += 1

        plt.xlabel(f'{variable} {disease}')
        plt.ylabel('Natural Log of Deaths per Million')
        plt.title(title)
        plt.legend(frameon=False, bbox_to_anchor=(1.05, 0.95), loc='upper left')
        plt.tight_layout()
        plt.savefig(
            os.path.join(saving_path, f'{disease}_deaths.png')
        )
        plt.close()


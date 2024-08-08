import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

class PLOT_POPULATION_DATA:
    def __init__(self):
        self.files_with_population_data = [x for x in os.listdir('Data/population_data_by_country') if x.endswith('.csv')]
        self.parent_dir = os.path.join(main_dir, 'Data/population_data_by_country')
        self.pyramids_results_dir = os.path.join(main_dir, 'Results/PYRAMIDS')
        self.percentage_results_dir = os.path.join(main_dir, 'Results/COMBINED_DISTRIBUTIONS')

        self.AGES = [
            '0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
            '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
            '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
            '90-94', '95-99', '100+'
        ]

    def run(self):
        for file_name in self.files_with_population_data:
            self.plotter(file_name)

    def plotter(self,file_name):
        data = pd.read_csv(os.path.join(self.parent_dir, file_name))
        data_frame = {
            'AGE': self.AGES,
            'MALES': data["male"],
            'FEMALES': data["female"],
            'TOTAL': data["total"],
            'PERCENTAGE' : []
        }

        total_population = data["total"].sum()
        percentages = [x/total_population * 100 for x in data["total"]]
        data_frame["PERCENTAGE"] = percentages
        
        self.age_groups = data_frame['AGE']
        self.males = data_frame['MALES']
        self.females = data_frame['FEMALES']
        self.percentages = data_frame['PERCENTAGE']

        self.make_pyramid(file_name)
        self.make_percentage_plot(file_name)   

    def make_pyramid(self,file_name):
        fig, ax = plt.subplots()
        ax.barh(self.age_groups, -self.males, color = 'blue',label = 'males', height = 0.9)

        ax.barh(self.age_groups, self.females, color = 'red',label = 'females', height = 0.9)
        
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        
        plt.tight_layout()
        file_name = file_name.split('.')[0]+'.png'
        plt.savefig(os.path.join(self.pyramids_results_dir, file_name))
        plt.close()
        print("Done plotting POPULATION PYRAMID for {}".format(file_name))

    def make_percentage_plot(self,file_name):
        fig, ax = plt.subplots()
        ax.plot(self.age_groups, self.percentages, color = 'blue',label = 'percentage')

        ax.set_xlabel('Age Group')
        ax.set_ylabel('Percentage')

        plt.xticks(rotation=50, ha='right')
        ax.grid(False)
        plt.tight_layout()
        plt.savefig(os.path.join(self.percentage_results_dir, file_name.split('.')[0]+'.png'))
        plt.close()
        print("Done plotting COMBINED DISTRIBUTIONS for {}".format(file_name))

    
if __name__ == "__main__":
    PLOT = PLOT_POPULATION_DATA()
    PLOT.run()
    
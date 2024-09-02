import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYSIS_FOR_OTHER_DISEASES.Analysis_of_Death_Data import MORTALITY_DATA
from ANALYSIS_FOR_OTHER_DISEASES.Death_data_Processor import DEATH_DATA_PROCESSOR
from ANALYSIS_FOR_OTHER_DISEASES.eval import EVAL

from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE
from ANALYSIS.Covid_Data_For_Date import COVID_DATA_FOR_DATE
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION

class ANALYSIS_FOR_OTHER_DISEASES:
    def __init__(self):
        pass

    def run(self):
        death_year = int(input('Enter Considering Death data year: '))
        COVID_DATA_FOR_DATE("2023-05-05")
        POPULATION_DATA_FOR_DATE(death_year)
        POP_CAL = POP_STAT_CALCULATION()
        POP_CAL.run()
        reference_country = input('Enter reference country: ')
        DEATH_DATA_PROCESSOR(death_year)
        data = MORTALITY_DATA(death_year, reference_country)
        data.ANALYZER()
        EVAL(reference_country)

    def parser_run(self, death_year, reference_country, selected: bool):
        DEATH_DATA_PROCESSOR(death_year)
        data = MORTALITY_DATA(death_year, reference_country)
        if selected:
            data.MORTALITY_DATA.ANALYZER_FOR_SELECTED_DISEASES()
        else:
            data.MORTALITY_DATA.ANALYZER()

if __name__ == '__main__':
    analysis = ANALYSIS_FOR_OTHER_DISEASES()
    analysis.run()
        

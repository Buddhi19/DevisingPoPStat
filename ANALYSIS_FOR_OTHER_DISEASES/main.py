import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYSIS_FOR_OTHER_DISEASES.Analysis_of_Death_Data import MORTALITY_DATA


def main():
    year = input("Enter the year(YYYY): ")
    mortality_data = MORTALITY_DATA(int(year))
    mortality_data.ANALYZER()

def selective_main():
    year = input("Enter the year(YYYY) or enter time period(YYYY-YYYY): ")
    if '-' in year:
        year = year.split('-')
        mortality_data = MORTALITY_DATA.ADD_RANGE(int(year[0]), int(year[1]))
    else:
        mortality_data = MORTALITY_DATA(int(year))
    mortality_data.ANALYZER_FOR_SELECTED_DISEASES()

if __name__ == "__main__":
    selective_main()
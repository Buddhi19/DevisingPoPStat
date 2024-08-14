import argparse
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS_FOR_OTHER_DISEASES.Analysis_of_Death_Data import MORTALITY_DATA

def main():
    parser = argparse.ArgumentParser(description="Analysis of Death Data")

    parser.add_argument("--y", type=int, help="Year for which data is to be analyzed")
    parser.add_argument("--c", type=str, help="Country for which data is to be analyzed")

    args = parser.parse_args()

    mortality_data = MORTALITY_DATA(args.y, args.c)
    mortality_data.ANALYZER()

if __name__ == "__main__":
    main()
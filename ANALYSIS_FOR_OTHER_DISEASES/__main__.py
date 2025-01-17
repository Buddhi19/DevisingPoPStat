import argparse
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS_FOR_OTHER_DISEASES.Analysis_of_Death_Data import MORTALITY_DATA

def main():
    parser = argparse.ArgumentParser(description="Analysis of Death Data")

    parser.add_argument("-y", type=str, help="Year/Span for which data is to be analyzed")
    parser.add_argument("-d", type=str, help="Disease for which data is to be analyzed")
    parser.add_argument("-ad", type=bool, help="Advanced Plotted")


    args = parser.parse_args()
    if "-" in args.y:
        global start,end,mortality_data
        start,end = args.y.split("-")
        mortality_data = MORTALITY_DATA.for_span(start,end)
        mortality_data.ANALYZER(advanced = args.ad)

    else:
        mortality_data = MORTALITY_DATA(args.y)
        mortality_data.ANALYZER()

if __name__ == "__main__":
    main()
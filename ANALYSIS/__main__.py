import argparse
import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.main import ANALYSIS

def main():
    parser = argparse.ArgumentParser(description="COVID-19 Analysis with POPSTAT COVID19")

    parser.add_argument("--py", type=int, help="Year for which population data is to be created")
    parser.add_argument("--cd", type=str, help="Date for which COVID data is to be created")
    parser.add_argument("--plot", type=str, help="Plot the data y or n")

    args = parser.parse_args()
    plot = True if args.plot == 'y' or args.plot == "Y" else False

    analysis = ANALYSIS()
    if args.py and args.cd:
        analysis.parser_run(args.py, args.cd, plot)
    elif args.py and not args.cd:
        analysis.parser_run(pop_year=args.py, plotter=plot)
    elif args.cd and not args.py:
        analysis.parser_run(covid_year=args.cd, plotter=plot)
    else:
        analysis.parser_run(plotter = plot)

if __name__ == "__main__":
    main()
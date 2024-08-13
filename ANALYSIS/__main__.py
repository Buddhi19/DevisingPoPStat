import argparse
from .main import ANALYSIS

def main():
    parser = argparse.ArgumentParser(description="COVID-19 Analysis with POPSTAT COVID19")

    parser.add_argument("--py", type=int, help="Year for which population data is to be created")
    parser.add_argument("--cd", type=str, help="Date for which COVID data is to be created")
    parser.add_argument("--plot", type=str, help="Plot the data y or n")

    args = parser.parse_args()
    plot = True if args.plot == 'y' or args.plot == "Y" else False

    analysis = ANALYSIS()
    analysis.parser_run(args.py, args.cd, plot)

if __name__ == "__main__":
    main()
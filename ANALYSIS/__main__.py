import argparse
from .main import ANALYSIS

def main():
    parser = argparse.ArgumentParser(description="COVID-19 Analysis with POPSTAT COVID19")

    parser.add_argument("--py", type=int, help="Year for which population data is to be created")
    parser.add_argument("--cd", type=str, help="Date for which COVID data is to be created")

    args = parser.parse_args()

    analysis = ANALYSIS()
    analysis.parser_run(args.py, args.cd)

if __name__ == "__main__":
    main()
# The application of population pyramid information for COVID-19 cases and deaths mortality POPULATION PYRAMID


## Setup the Environment

### Clone the Repository
```bash
git clone https://github.com/Buddhi19/Pop_Pyramid.git
cd Pop_Pyramid
```

### Download Dependencies and Setup Workspace
```bash
bash ./setup_environment.sh
```

## 📥 Download Data from Here

- 👶 [**Age Dataset**](https://population.un.org/wpp2019/Download/Standard/CSV/)
- 🦠 [**Owid Covid Dataset**](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv)
- 📊 [**Median Age**](https://ourworldindata.org/grapher/median-age?tab=table)
- 📈 [**SDI**](https://www.graham-center.org/maps-data-tools/social-deprivation-index.html)
- 🌍 [**HDI**](https://ourworldindata.org/grapher/human-development-index?tab=table)
- 💰 [**GDP per Capita**](https://ourworldindata.org/grapher/gdp-per-capita-maddison?tab=table)
- 🌡️ [**Life Expectancy**](https://ourworldindata.org/grapher/life-expectancy?tab=table)
- 🏙️ [**Population Density**](https://ourworldindata.org/grapher/population-density?tab=table)

After downloading, place the files in the appropriate directories as shown in the folder structure below.

## Folder Structure

Ensure your folder structure looks like this:

```
📊 Pop_Pyramid
│
├── 📈 ANALYSIS
├── 🔬 ANALYSIS_FOR_OTHER_DISEASES
├── 📁 DATA
│   ├── 🌍 countries
│   ├── 🦠 covid_data_by_country
│   ├── ⚰️ deaths_by_cause
│   ├── ⚰️ deaths_by_cause_per_country
│   ├── 🗂️ owid_covid_data
│   │   └── 📄 owid-covid-data.csv
│   ├── 🗂️ owid_data
│   │   ├── 📄 median-age.csv
│   │   ├── 📄 population-density.csv
│   │   ├── 📄 life-expectancy.csv
│   │   ├── 📄 gdp-per-capita.csv
│   │   ├── 📄 human-development-index.csv
│   │   └── 📄 sdi_data.csv
│   ├── 🗂️ death_data
│   │   └── 📄 deaths_by_cause.csv
│   ├── 👥 population_data_by_country
│   └── 👶👴 population_data_with_age
│       └── 📄 age_data.csv
└── 📊 RESULTS
    ├── 📊 COMBINED_DISTRIBUTIONS
    ├── 🧮 POPSTATCOVID
    ├── 🧮 POPSTAT_COUNTRY_DATA
    └── 🏛️ PYRAMID
```

## Running the Analysis for COVID Data

Choose your analysis parameters:

1. Population Year: ____ (e.g., 2020)
2. Covid Data Date: ____ (format: YYYY-MM-DD, e.g., 2022-04-08)
3. Plot population pyramids? (y/n): 

Now, run the analysis with your chosen parameters:

```python
python -m ANALYSIS --py <population year> --cd "<covid data date>" --plot "<y/n>"
```

For example:
```python
python -m ANALYSIS --py 2020 --cd "2022-04-08" --plot "y"
```

## View Results

After running the analysis, check the `RESULTS` folder for your output files and visualizations.

## Need Help?

If you encounter any issues or have questions, please open an issue on the GitHub repository

### Happy analyzing! 🚀📊
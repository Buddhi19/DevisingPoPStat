# The application of population pyramid information for COVID-19 cases and deaths mortality POPULATION PYRAMID

## 1. Setup the Environment

Clone the Repository
  ```
git clone https://github.com/Buddhi19/Pop_Pyramid.git
  ```
Download all dependencies and setup workspace

  ```
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



## The Folder Structure should look like

```
# 📊 Pop_Pyramid
│
├── 📈 ANALYSIS
├── 🔬 ANALYSIS_FOR_OTHER_DISEASES
├── 📁 DATA
│   ├── 🌍 countries
│   ├── 🦠 covid_data_by_country
│   ├── ⚰️ deaths_by_cause
│   ├── ⚰️ deaths_by_cause_per_country
│   ├── 🗂️ owid_covid_data
│   │   └── 📄 owid-covid-data.csv (downloaded file)
│   │
│   ├── 🗂️ owid_data
│   │   └── 📄 median-age.csv (downloaded file)
│   │   └── 📄 population-density.csv (downloaded file)
│   │   └── 📄 life-expectancy.csv (downloaded file)
│   │   └── 📄 gdp-per-capita.csv (downloaded file)
│   │   └── 📄 human-development-index.csv (downloaded file)
│   │   └── 📄 sdi_data.csv (downloaded file)
│   │
│   ├── 🗂️ death_data
│   │   └── 📄 deaths_by_cause.csv (downloaded file)
│   │
│   ├── 👥 population_data_by_country
│   └── 👶👴 population_data_with_age
│       └── 📄 age_data.csv (downloaded file)
│
└── 📊 RESULTS
    ├── 📊 COMBINED_DISTRIBUTIONS
    ├── 🧮 POPSTATCOVID
    ├── 🧮 POPSTAT_COUNTRY_DATA
    └── 🏛️ PYRAMID
```

## 2. Running the ANALYSIS for COVID Data
1. On the Current Directory
    
    ```python 
    python -m ANALYSIS --py <population year(YYYY)> 
                        --cd "<covid data (YYYY-MM-DD)>"
                         --plot "<y/n>"
    ```
    ### Population Year as per the paper : 2020
    ### Covid Date as per the paper : 2022-04-08
    ### Plot population pyramids : y

    ```python
    python -m ANALYSIS --py 2020 --cd "2022-04-08" --plot "y"
    ```

2. Or just simply run the main.py file

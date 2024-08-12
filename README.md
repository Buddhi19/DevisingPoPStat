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

## If data not properly downloaded manually download from here

[Age Dataset](https://population.un.org/wpp2019/Download/Standard/CSV/)

[Owid Covid Dataset](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv)

## The Folder Structure should look like

```
Pop_Pyramid
│
├── ANALYSIS
├── ANALYSIS_FOR_OTHER_DISEASES
├── DATA
│   ├── countries
│   ├── covid_data_by_country
│   ├── deaths_by_cause
│   ├── deaths_by_cause_per_country
│   ├── owid_covid_data
│   │   └── owid-covid-data.csv (downloaded file)
│   ├── population_data_by_country
│   └── population_data_with_age
│       └── age_data.csv (downloaded file)
│
└── RESULTS
    ├── COMBINED_DISTRIBUTIONS
    ├── POPSTATCOVID
    ├── POPSTAT_COUNTRY_DATA
    └── PYRAMID
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
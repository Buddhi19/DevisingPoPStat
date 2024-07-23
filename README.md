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
## If you are encountering errors due to Windows-style line endings (CRLF),try followings.

**VS Code**
1. Open the file in VS Code.
2. In the bottom-right corner, click on the text that says `CRLF`.
3. Select `LF` from the menu.
4. Save the file.

**Notepad++**
1. Open the file in Notepad++.
2. Go to `Edit` > `EOL Conversion` > `Unix (LF)`.
3. Save the file.

**If you are using LINUX**
1. Install dos2unix
    ```sh
    sudo apt-get install dos2unix
2. Run the command
   ```sh
   dos2unix ./setup_environment.sh
   ```

**If you are using WSL**
1. Run the command
    ```sh
    sed -i 's/\r$//' ./setup_environment.sh
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

## 2. Implementation Description


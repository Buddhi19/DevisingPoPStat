# Devising PoPStat: A metric bridging population pyramids with global disease mortality

## Abstract
Understanding the relationship between population dynamics and disease-specific mortality is central to evidence-based health policy. This study introduces two novel metrics, PoPDivergence and PoPStat, one to quantify the difference between population pyramids and the other to assess the strength and nature of their association with the mortality of a given disease. PoPDivergence, based on Kullback-Leibler divergence, measures deviations between a country’s population pyramid and a reference pyramid. PoPStat is the correlation between these deviations and the log form of disease-specific mortality rates. The reference population is selected by a brute-force optimization that maximizes this correlation.  Utilizing mortality data from the Global Burden of Disease 2021 and population statistics from the United Nations, we applied these metrics to 371 diseases across 204 countries. Results reveal that PoPStat outperforms traditional indicators such as median age, GDP per capita, and Human Development Index in explaining the mortality of most diseases. Noncommunicable diseases (NCDs) like neurological disorders and cancers, communicable diseases (CDs) like neglected tropical diseases, and maternal and neonatal diseases were tightly bound to the underlying demographic attributes whereas NCDs like diabetes, CDs like respiratory infections and injuries including self-harm and interpersonal violence were weakly associated with population pyramid shapes. Notably, except for diabetes, the NCD mortality burden was shared by constrictive population pyramids, while mortality of communicable diseases, maternal and neonatal causes and injuries were largely borne by expansive pyramids. Therefore, PoPStat provides insights into demographic determinants of health and empirical support for models on epidemiological transition. By condensing the multi-dimensional population pyramid to a scalar variable, PoPDivergence allows us to examine the relationship of any variable of interest with the underlying population structure. These metrics have the potential to advance future global health and population research.

## [Find Our Paper Here](https://arxiv.org/abs/2501.11514)

---

## 🚀 Setup the Environment

### 📂 Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/Buddhi19/Pop_Pyramid.git
cd Pop_Pyramid
```

### 🔧 Download Dependencies and Setup Workspace
Run the setup script to install dependencies and prepare the workspace:
```bash
bash ./setup_environment.sh
```

---

## 📥 Download Data

The following datasets are required for analysis. Download them and place them in their respective folders as outlined below:

- 👶 [**Age Dataset**](https://population.un.org/wpp2019/Download/Standard/CSV/)
- 🦠 [**Owid COVID Dataset**](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv)
- 📊 [**Median Age**](https://ourworldindata.org/grapher/median-age?tab=table)
- 📈 [**SDI**](https://www.graham-center.org/maps-data-tools/social-deprivation-index.html)
- 🌍 [**HDI**](https://ourworldindata.org/grapher/human-development-index?tab=table)
- 💰 [**GDP per Capita**](https://ourworldindata.org/grapher/gdp-per-capita-maddison?tab=table)
- 🌡️ [**Life Expectancy**](https://ourworldindata.org/grapher/life-expectancy?tab=table)
- 🏙️ [**Population Density**](https://ourworldindata.org/grapher/population-density?tab=table)
- ⚰️ [**Mortality Data**](https://vizhub.healthdata.org/gbd-results/)

Alternatively, download the pre-structured data folder from [Google Drive](https://drive.google.com/drive/folders/1-0MWgPvg8C7oSzcWMlH5UEoBzkjJ4G5Y?usp=sharing).

---

## 📂 Folder Structure

Organize your downloaded data to match the following structure:

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
```

---

## 🛠️ Running the Analyses

### 🔍 Analyze COVID Data
Set your parameters and run the analysis:

1. **Population Year**: Enter the year for population data (e.g., `2020`).
2. **COVID Data Date**: Enter the desired date for COVID data (format: `YYYY-MM-DD`, e.g., `2022-04-08`).
3. **Plot Population Pyramids**: Choose whether to generate visualizations (`y/n`).

Run the analysis:
```bash
python -m ANALYSIS --py <population year> --cd "<covid data date>" --plot "<y/n>"
```

#### Example Command:
```bash
python -m ANALYSIS --py 2020 --cd "2022-04-08" --plot "y"
```

### 🔍 Analyze All Diseases
To analyze death data for all diseases:
```bash
python ANALYSIS_FOR_OTHER_DATA/Analysis_of_Death_Data.py
```

---

## 📊 View Results

After running the analyses, output files and visualizations will be saved in the `RESULTS` folder. Review these for insights and further interpretation.

---

## ❓ Need Help?
If you encounter any issues or have questions, feel free to [open an issue](https://github.com/Buddhi19/Pop_Pyramid/issues) on the GitHub repository.

---

### 🎉 Happy Analyzing! 🚀📊
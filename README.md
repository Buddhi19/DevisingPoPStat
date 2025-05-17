# Devising PoPStat: A metric bridging population pyramids with global disease mortality

## Abstract

**Background** Traditional demographic indicators offer a limited view of a country’s population structure and may not
capture demographic influences on mortality patterns comprehensively. We aimed to bridge this gap by developing
novel scalar metrics that condense the information in population pyramids and assess their association with disease
specific mortality.


**Methods** Country specific population pyramids were constructed using the United Nations World Population Prospects
2024, while mortality data for 371 diseases across 180 countries were extracted from the Global Burden of Disease
Study 2021. We then developed two metrics: PoPDivergence, which quantifies the difference between a country’s
population pyramid and an optimized reference pyramid using Kullback Leibler divergence, and PoPStat, which is the
correlation between PoPDivergence and cause specific mortality rates.


**Findings** Non communicable diseases (NCDs) showed a strong PoPStat of –0.84 (optimized reference: Japan, p<0.001)
with mortality concentrated to constrictive pyramids. Communicable, maternal, neonatal, and nutritional diseases
had a moderate PoPStat of 0.50 (Singapore, p<0.001) with mortality linked to expansive pyramids. Injuries exhibited
a weak PoPStat (0.291, Singapore, < 0.001). In more granular analyses, NCDs like neurological disorders and
neoplasms, communicable diseases (CDs) like neglected tropical diseases, and other infections showed a strong PoPStat.
Nevertheless, NCDs like diabetes, cirrhosis, and other chronic liver diseases, CDs like respiratory infections and
tuberculosis carried a weak PoPStat indicating minimal influence of population pyramid on their mortality.
Interpretations This study, its devised metrics, demonstrates the degree to which the mortality of different diseases
is bound to the underlying population structure and reveals what type of population pyramids will carry the highest
mortality attributed to those diseases.


**Funding** This study received no external funding.


**Keywords** Population Pyramids, Demographic Transition, Epidemiology, PopDivergence, PoPStat

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

Alternatively, download the pre-structured data folder from [Google Drive](https://drive.google.com/drive/folders/1w31NAs-HzlxPql89kmXfEh3liHzjt0S1?usp=sharing).

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

import pandas as pd

# Load the data
print("Loading data...")
location_map = pd.read_csv('./DATA/countries/country_names_map.csv')
death_data = pd.read_csv('./DATA/death_data/raw/IHME-GBD_2021_DATA-d1938792-1.csv')
age_data = pd.read_csv('./DATA/population_data_with_age/age_data.csv')
print("Data loaded successfully.")

# Process death data
print("Processing death data...")
death_data = death_data[(death_data['metric_id'] == 1) & (death_data['measure_name'] == 'Deaths')]
death_data = death_data.drop(columns=['metric_id', 'metric_name', 'measure_name', 'upper', 'lower', 'cause_id', 'cause_name', 'measure_id', 'location_id', 'age_id', 'age_name'])
death_data = death_data.groupby(['location_name', 'year']).agg({'val': 'sum'}).reset_index()
death_data['val'] = death_data['val'].astype(int)
death_data_pivoted = death_data.pivot(index='location_name', columns='year', values='val').reset_index()
death_data_pivoted['location_name'] = death_data_pivoted['location_name'].str.lower()
death_data_pivoted = death_data_pivoted[death_data_pivoted['location_name'].isin(location_map['death_data'])].reset_index(drop=True)
death_data_pivoted['location_name'] = death_data_pivoted['location_name'].map(location_map.set_index('death_data')['Country'])
death_data_pivoted = death_data_pivoted.rename(columns={'location_name': 'country'})
death_data_pivoted = death_data_pivoted.sort_values('country').reset_index(drop=True)
death_data_pivoted.columns.name = None
print("Death data processed successfully.")

# Process age data
print("Processing age data...")
age_data = age_data[(age_data['Time'] >= 1980) & (age_data['Time'] <= 2021)]
age_data = age_data.groupby(['Location', 'Time']).agg({'PopTotal': 'sum'}).reset_index()
age_data['PopTotal'] = age_data['PopTotal'].astype(int)
age_data_pivoted = age_data.pivot(index='Location', columns='Time', values='PopTotal').reset_index()
age_data_pivoted.columns.name = None
age_data_pivoted['Location'] = age_data_pivoted['Location'].str.lower()
age_data_pivoted = age_data_pivoted[age_data_pivoted['Location'].isin(location_map['location'])].reset_index(drop=True)
age_data_pivoted['Location'] = age_data_pivoted['Location'].map(location_map.set_index('location')['Country'])
age_data_pivoted = age_data_pivoted.rename(columns={'Location': 'country'})
age_data_pivoted = age_data_pivoted.sort_values('country').reset_index(drop=True)
print("Age data processed successfully.")

# Calculate deaths per million
print("Calculating deaths per million...")
deaths_per_million = death_data_pivoted.copy()
for i in range(1, len(deaths_per_million.columns)):
    deaths_per_million.iloc[:, i] = round((deaths_per_million.iloc[:, i] / age_data_pivoted.iloc[:, i]) * 1000, 2)
print("Deaths per million calculated successfully.")

# Save the results
print("Saving results...")
deaths_per_million.to_csv('./DATA/death_data/processed/all_cause_death_data_history_dpm.csv', index=False)
print("Results saved successfully.")

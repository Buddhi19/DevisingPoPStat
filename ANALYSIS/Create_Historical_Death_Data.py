import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('./DATA/death_data/raw/IHME-GBD_2021_DATA-8df82d8f.csv')
country_map = pd.read_csv('./DATA/countries/country_names_map.csv')
age_data = pd.read_csv('./DATA/population_data_with_age/age_data.csv')
print("Data loaded successfully.")

# Process age data
print("Processing age data...")
age_data = age_data[(age_data['Time'] >= 1980) & (age_data['Time'] <= 2021)]
age_data = age_data.groupby(['Location', 'Time']).agg({'PopTotal': 'sum'}).reset_index()
age_data['PopTotal'] = age_data['PopTotal'].astype(int)
age_data_pivoted = age_data.pivot(index='Location', columns='Time', values='PopTotal').reset_index()
age_data_pivoted.columns.name = None
age_data_pivoted['Location'] = age_data_pivoted['Location'].str.lower()
age_data_pivoted = age_data_pivoted[age_data_pivoted['Location'].isin(country_map['location'])].reset_index(drop=True)
age_data_pivoted['Location'] = age_data_pivoted['Location'].map(country_map.set_index('location')['Country'])
age_data_pivoted = age_data_pivoted.rename(columns={'Location': 'country'})
age_data_pivoted = age_data_pivoted.sort_values('country').reset_index(drop=True)
print("Age data processed successfully.")

# Calculate average population for the years 2018-2021
print("Calculating average population for 2018-2021...")
new_pop_data = pd.DataFrame()
new_pop_data['country'] = age_data_pivoted['country']
new_pop_data['pop'] = age_data_pivoted[[2018, 2019, 2020, 2021]].mean(axis=1).astype(float)
new_pop_data = new_pop_data.sort_values('country').reset_index(drop=True)
print("Average population calculated successfully.")

# Process death data
print("Processing death data...")
df = df.groupby(['location_name', 'cause_name'])['val'].mean().reset_index()
df_pivot = df.pivot(index='location_name', columns='cause_name', values='val').reset_index()
df_pivot.columns.name = None
df_pivot['location_name'] = df_pivot['location_name'].str.lower()
df_pivot = df_pivot.sort_values('location_name').reset_index(drop=True)
df_pivot = df_pivot[df_pivot['location_name'].isin(country_map['death_data'])].reset_index(drop=True)
df_pivot['location_name'] = df_pivot['location_name'].map(country_map.set_index('death_data')['Country'])
df_pivot = df_pivot.sort_values('location_name').reset_index(drop=True)
print("Death data processed successfully.")

# Calculate deaths per million
print("Calculating deaths per million...")
for col in df_pivot.columns[1:]:
    df_pivot[col] = round(df_pivot[col] / new_pop_data['pop'] * 1000, 2)
print("Deaths per million calculated successfully.")

# Save the results
print("Saving results...")
df_pivot.to_csv('./DATA/death_data/processed/death_data_history_dpm.csv', index=False)
print("Results saved successfully.")

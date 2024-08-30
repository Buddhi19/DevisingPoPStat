#!/bin/bash

# Get the absolute path of the directory where the script is located
script_dir=$(dirname "$(realpath "$0")")

# Function to execute commands with confirmation
execute_with_confirmation() {
    local command=$1
    read -p "Do you want to execute the command: $command (y/n)? " choice
    if [[ "$choice" = "y" || "$choice" = "Y" ]]; then
        echo "Executing command: $command"
        eval $command
        echo "Command executed successfully"
    else
        echo "Command not executed"
    fi
}

# Function to make directories in the script directory
make_directories() {
    mkdir -p "$script_dir/DATA/death_data" 
    mkdir -p "$script_dir/DATA/covid_data_by_country" 
    mkdir -p "$script_dir/DATA/owid_covid_data"
    mkdir -p "$script_dir/DATA/population_data_by_country"
    mkdir -p "$script_dir/DATA/population_data_with_age"
    mkdir -p "$script_dir/DATA/death_data"
    mkdir -p "$script_dir/DATA/owid_data"
    mkdir -p "$script_dir/DATA/owid_data_filtered"
}

# Function to load data
load_data() {
    wget -O "$script_dir/DATA/owid_covid_data/owid-covid-data.csv" "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
}

# Function to make directories for POPSTAT
make_directory_for_POPSTAT() {
    mkdir -p "$script_dir/RESULTS/POPSTAT_COUNTRY_DATA" 
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/POPSTAT"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS"

    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/GDP_PER_CAPITA"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/POPULATION_DENSITY"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/GINI"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/HDI"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/LIFE_EXPECTANCY"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/SDI"
    mkdir -p "$script_dir/RESULTS/CORRELATION_WITH_OTHER_DISEASES/OTHER_METRICS/UHCI"

    mkdir -p "$script_dir/RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/cases"
    mkdir -p "$script_dir/RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/deaths"
    mkdir -p "$script_dir/RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/cases"
    mkdir -p "$script_dir/RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/deaths"
    mkdir -p "$script_dir/RESULTS/POPSTATCOVID/OTHER_METRICS"
}

execute_with_confirmation "pip install -r requirements.txt"
execute_with_confirmation "make_directories"
execute_with_confirmation "load_data"
execute_with_confirmation "make_directory_for_POPSTAT"
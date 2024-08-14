#!/bin/bash

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


# Function to make directories in the current directory
make_directories() {
    local current_dir=$(pwd)
    cd "$current_dir"
    mkdir -p "DATA/death_data" 
    mkdir -p "DATA/covid_data_by_country" 
    mkdir -p "DATA/owid_covid_data"
    mkdir -p "DATA/population_data_by_country"
    mkdir -p "DATA/population_data_with_age"
    mkdir -p "DATA/death_data"
    mkdir -p "DATA/owid_data"
}

# Function to load data
load_data() {
    local current_dir=$(pwd)
    cd "$current_dir"
    wget -O DATA/owid_covid_data/owid-covid-data.csv "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
}

make_directory_for_POPSTAT(){
    local current_dir=$(pwd)
    cd "$current_dir"
    mkdir -p "RESULTS/POPSTAT_COUNTRY_DATA" 
    mkdir -p "RESULTS/CORRELATION_WITH_OTHER_DISEASES"
    mkdir -p "RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES"
    mkdir -p "RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/cases"
    mkdir -p "RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/deaths"
    mkdir -p "RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/cases"
    mkdir -p "RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/deaths"
    mkdir -p "RESULTS/POPSTATCOVID/OTHER_METRICS"
}

execute_with_confirmation "pip install -r requirements.txt"
execute_with_confirmation "make_directories"
execute_with_confirmation "load_data"
execute_with_confirmation "make_directory_for_POPSTAT"
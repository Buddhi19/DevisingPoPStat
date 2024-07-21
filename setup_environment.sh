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

# Function to install prerequisites
install_pre_requisites() {
    execute_with_confirmation "pip install -r requirements.txt"
}

# Function to make directories in the current directory
make_directories() {
    global current_dir=$(pwd)
    cd "$current_dir"
    mkdir -p "DATA/countries" "DATA/covid_data_by_country" "DATA/owid_covid_data" "DATA/population_data_by_country" "DATA/population_data_with_age"
}

# Function to load data
load_data() {
    cd "$current_dir"
    wget -O /DATA/owid_covid_data/owid-covid-data.csv https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv
    wget -O /DATA/population_data_with_age/age_data.csv "https://population.un.org/wpp2019/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_PopulationByAgeSex_Medium.csv"
}

make_directory_for_POPSTAT(){
    cd "$current_dir/RESULTS"
    mkdir -p "POPSTAT_COUNTRY_DATA"
}

install_pre_requisites
make_directories
execute_with_confirmation "load_data"
make_directory_for_POPSTAT
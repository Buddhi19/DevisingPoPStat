import sys
import os

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from ANALYSIS_FOR_OTHER_DISEASES.Analysis_of_Death_Data import MORTALITY_DATA
from ANALYSIS_FOR_OTHER_DISEASES.ALL_PATHS_DATA import *

def CSV_FOR_PAPER():
    diseases = [
            "Ischemic heart disease",
            "Stroke",
            "Pulmonary Arterial Hypertension",
            "Chronic obstructive pulmonary disease",
            "Asthma",
            "Breast cancer",
            "Colon and rectum cancer",
            "Cervical cancer",
            "Prostate cancer",
            "Liver cancer",
            "Cirrhosis and other chronic liver diseases",
            "Inflammatory bowel disease",
            "Alzheimer's disease and other dementias",
            "Parkinson's disease",
            "Alcohol use disorders",
            "Diabetes mellitus",
            "Chronic kidney disease",
            "Rheumatoid arthritis",
            "Maternal disorders",
            "Neonatal disorders",
            "Self-harm",
            "Interpersonal violence",
            "HIV/AIDS",
            "Tuberculosis",
            "Dengue",
            "Protein-energy malnutrition"
        ]
    M = MORTALITY_DATA(2021)
    for disease in diseases:
        M.filter_death_data(disease)
        M.create_dataframe_for_diseases(disease,True)

    M.CLOSEST_COUNTRIES = pd.DataFrame(M.CLOSEST_COUNTRIES)
    M.CLOSEST_COUNTRIES.to_csv(
        os.path.join(SAVING_PATH_CSV_FOR_YEAR(str(2021)), "Correlation_Selected.csv"), index = False
    )
    

if __name__ == "__main__":
    CSV_FOR_PAPER()
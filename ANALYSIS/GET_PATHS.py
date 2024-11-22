import os
import sys

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

def get_case_dir(year:str):
    path = os.path.join(main_dir, "RESULTS",f"FOR_COVID_UI_{year}","CASE_DATA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_death_dir(year:str):
    path = os.path.join(main_dir, "RESULTS",f"FOR_COVID_UI_{year}","DEATH_DATA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_popstat_dir(year:str):
    path = os.path.join(main_dir, "RESULTS",f"FOR_COVID_UI_{year}","POPSTAT_DATA")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_pyramids_dir(year:str):
    path = os.path.join(main_dir, "RESULTS",f"FOR_COVID_UI_{year}","PYRAMIDS")
    if not os.path.exists(path):
        os.makedirs(path)
    return path
import os
import json
import pandas as pd
import numpy as np
import pdfplumber
import re

import trees_data

def load_config(json_file="./green_data/trees_absorption.json"):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

def old_tree(time, co2_amount: float):
    # ile CO2 pochłonie jedno 100-letnie drzewo w okreslonym czasie
    # time to ilosc dni

    old_tree_absorption_const = load_config()["old_tree_absorption"]  # kg CO2 rocznie przez 100-letnie drzewo
    daily_absorption = old_tree_absorption_const/365
    # years_absorption = co2_amount / old_tree_absorption_const
    # days_needed = years_absorption * 365  # Zakładamy rok kalendarzowy o 365 dniach

    return daily_absorption * time


def middle_tree(time, co2_amount: float):
    # ile drzew sredniej wielkości jest w stanie pochłonąac ich emisje w jednym okresie wegetacyjnym.
    middle_tree_absorption_in_summer_const = load_config()["middle_tree_absorption"]

    middle_tree_count = int(co2_amount / middle_tree_absorption_in_summer_const)

    return middle_tree_count


def young_tree(time: int, co2_amount: float):
    # ile małych sadzonek byłoby potrzebnych do pochlonięcia wyemitowanych CO2 w danym czasie.
    young_tree_absorption = load_config()["young_tree_absorption"]  # kg CO2 rocznie

    # Obliczanie, ile CO2 pochłonie jedna sadzonka w podanym czasie
    young_tree_absorption_in_time = young_tree_absorption * time

    # Obliczanie liczby sadzonek potrzebnych do skompensowania podanej ilości CO2 w danym czasie
    young_tree_count = co2_amount / young_tree_absorption_in_time

    return young_tree_count


def main():
    print(old_tree(30, 300))
    print(middle_tree(1, 300))
    print(young_tree(100, 300))

if __name__ == '__main__':
    main()





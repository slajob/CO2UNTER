import os
import json
import pandas as pd
import numpy as np
import pdfplumber
import re
import random
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

def remove_null_values(data):
    return {key: value for key, value in data.items() if value['co2_absorpcja'] is not None}

def get_random_key(data):
    return random.choice(list(data.keys()))

def parks_absorption(co2_amount: float):
    # parki_pdf_file_path = "./green_data/Parki.pdf"
    # parki_data = trees_data.read_pdf_data(parki_pdf_file_path)
    # parki_df = trees_data.create_parki_df(parki_data)

    parki_absorption_file_path = "./green_data/parks_absorption.json"
    parki_absorption_data = load_config(parki_absorption_file_path)
    filtered_data = remove_null_values(parki_absorption_data)

    random_park_name = get_random_key(filtered_data)  # Losowy klucz
    random_park_data = filtered_data[random_park_name]

    # print(f'random_park_data: {random_park_data}')
    number_of_trees = random_park_data['ilosc drzew']
    yearly_co2_absorption = random_park_data['co2_absorpcja']
    monthly_co2_absrption = yearly_co2_absorption/12

    percentage_of_park = np.round((co2_amount / monthly_co2_absrption) * 100, 2)

    # Oblicz liczbę drzew potrzebnych do zniwelowania CO2
    trees_needed = int((co2_amount / (monthly_co2_absrption / number_of_trees)))

    # print(f'potrzzba zniwelować: {co2_amount}')

    # print(f'{random_park_name}, potrzeba {percentage_of_park}% parku to jest {trees_needed} drzew')

    return random_park_name, percentage_of_park, trees_needed


def main():
#     Kraków
#     ": {
#     "ilosc drzew": 101159,
#     "co2_absorpcja": 6423000
#
# }
    print(old_tree(30, 300))
    print(middle_tree(1, 300))
    print(young_tree(100, 300))

    parks_absorption(300)
    parks_absorption(10)
    parks_absorption(300000)



if __name__ == '__main__':
    main()





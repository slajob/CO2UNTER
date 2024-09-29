import json
import numpy as np
import random
import trees_data


def load_config(json_file="./green_data/trees_absorption.json"):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

def old_tree(time):
    # ile CO2 pochłonie jedno 100-letnie drzewo w okreslonym czasie
    # time to ilosc dni

    old_tree_absorption_const = load_config()["old_tree_absorption"]  # kg CO2 rocznie przez 100-letnie drzewo
    daily_absorption = old_tree_absorption_const/365
    # years_absorption = co2_amount / old_tree_absorption_const
    # days_needed = years_absorption * 365  # Zakładamy rok kalendarzowy o 365 dniach

    return np.round(daily_absorption * time, 2)


def middle_tree(co2_amount: float):
    # ile drzew sredniej wielkości jest w stanie pochłonąac ich emisje w jednym okresie wegetacyjnym.
    middle_tree_absorption_in_summer_const = load_config()["middle_tree_absorption"]

    middle_tree_count = int(co2_amount / middle_tree_absorption_in_summer_const)

    return middle_tree_count


def young_tree(time: int, co2_amount: float):
    # ile małych sadzonek byłoby potrzebnych do pochlonięcia wyemitowanych CO2 w danym czasie.
    young_tree_absorption = load_config()["young_tree_absorption"]  # kg CO2 rocznie

    # Obliczanie, ile CO2 pochłonie jedna sadzonka w podanym czasie
    young_tree_absorption_in_time = young_tree_absorption/365 * time

    # Obliczanie liczby sadzonek potrzebnych do skompensowania podanej ilości CO2 w danym czasie
    young_tree_count = int(co2_amount / young_tree_absorption_in_time)

    return young_tree_count

def remove_null_values(data):
    return {key: value for key, value in data.items() if value['co2_absorpcja'] is not None}

def get_random_key(data):
    return random.choice(list(data.keys()))

def parks_absorption(co2_amount: float):
    parki_pdf_file_path = "./green_data/Parki.pdf"
    parki_data = trees_data.read_pdf_data(parki_pdf_file_path)
    parki_df = trees_data.create_parki_df(parki_data)

    parki_absorption_file_path = "./green_data/parks_absorption.json"
    parki_absorption_data = load_config(parki_absorption_file_path)
    filtered_data = remove_null_values(parki_absorption_data)

    random_park_name = get_random_key(filtered_data)  # Losowy klucz
    random_park_data = filtered_data[random_park_name]

    number_of_trees = random_park_data['ilosc drzew']
    yearly_co2_absorption = random_park_data['co2_absorpcja']
    monthly_co2_absrption = yearly_co2_absorption/12

    filtered_park = parki_df[parki_df['NAZWA PARKU'] == random_park_name]
    # Oblicz procent parku potrzebny do zniwelowania CO2
    percentage_of_park = np.round((co2_amount / monthly_co2_absrption) * 100, 2)
    # Oblicz liczbę drzew potrzebnych do zniwelowania CO2
    trees_needed = int((co2_amount / (monthly_co2_absrption / number_of_trees)))


    return_data = {'nazwa_parku': random_park_name,
                   'procent_powierzchni': percentage_of_park,
                   'potrzebne_drzewa': trees_needed,
                   'pelna_powierzchnia': None,
                   'powierznia_potrzebna': None
                   }

    # Sprawdź, czy park istnieje w pliku pdf
    if not filtered_park.empty:
        park_full_area = float(filtered_park['POW (ha)'].values[0].replace(',', '.'))
        park_needed_area = np.round((percentage_of_park/100) * park_full_area, 2)
        return_data['pelna_powierzchnia'] = park_full_area
        return_data['powierznia_potrzebna'] = park_needed_area
    else:
        return_data['pelna_powierzchnia'] = 'Brak danych'
        return_data['powierznia_potrzebna'] = 'Brak danych'

    return return_data


def main():
    print(young_tree(30, 5656))
    print(parks_absorption(4335))

if __name__ == '__main__':
    main()





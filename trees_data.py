import os
import json
import pandas as pd
import numpy as np
import pdfplumber
import re

def parse_park_line(line):
    # Sprawdzenie czy linia ma poprawny format (kończy się liczbą z przecinkiem)
    if re.search(r"\d+,\d+$", line):
        # Wyciągnięcie indeksu
        index_match = re.match(r"(\d+)\.", line)
        index = index_match.group(1) if index_match else None

        # Usunięcie indeksu
        line = re.sub(r"^\d+\.\s*", "", line)

        # Wyciągnięcie powierzchni (ostatnia liczba w linii)
        pow_match = re.search(r"(\d+,\d+)$", line)
        pow_ha = pow_match.group(1) if pow_match else None

        # Usunięcie powierzchni z linii
        line = re.sub(r"\s*\d+,\d+$", "", line)

        # Wyciągnięcie dzielnicy (liczba rzymska i tekst dzielnicy)
        dzielnica_match = re.search(r"([IVXLCDM]+\s+\w+(?:\s*\-\s*\w+)?)$", line)
        dzielnica = dzielnica_match.group(1) if dzielnica_match else None

        # Usunięcie dzielnicy z linii
        line = re.sub(r"\s*[IVXLCDM]+\s+\w+(?:\s*\-\s*\w+)?$", "", line)

        # Reszta linii to nazwa parku
        nazwa_parku = line.strip()

        # Zwrócenie podzielonej linii jako lista
        return [index, nazwa_parku, dzielnica, pow_ha]

    # Jeśli linia jest niepoprawna, pomijamy ją
    return None


def create_parki_df(all_text):
    park_data = []
    all_text = all_text.split('\n')
    for line in all_text:
        parsed_data = parse_park_line(line)
        if parsed_data:  # Dodajemy tylko poprawne wiersze
            park_data.append(parsed_data)

    park_df = pd.DataFrame(park_data, columns=['INDEX', 'NAZWA PARKU', 'DZIELNICA', 'POW (ha)'])

    return park_df


def read_pdf_data(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text()

    return all_text



def main():

    parki_pdf_file_path = "./green_data/Parki.pdf"
    parki_data = read_pdf_data(parki_pdf_file_path)
    parki_df = create_parki_df(parki_data)

    parki_kiesz_pdf_file_path = "./green_data/parki kieszonkowe 6.24.pdf"
    parki_kiesz_data = read_pdf_data(parki_kiesz_pdf_file_path)
    parki_kiesz_df = create_parki_df(parki_kiesz_data)

    print(parki_kiesz_df)

if __name__ == '__main__':
    main()




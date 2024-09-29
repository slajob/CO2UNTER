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
        # dzielnica_match = re.search(r"(\s+[IVXLCDM]+\s+\w+(?:\s*\-\s*\w+)?)$", line)
        nazwa_parku_match = re.search(r"^(.*?)(?=\s[IVXLCDM]+(?:,|\s|$))", line)
        nazwa_parku = nazwa_parku_match.group(1) if nazwa_parku_match else None

        # Usunięcie dzielnicy z linii
        line = re.sub(r"^(.*?)(?=\s[IVXLCDM]+(?:,|\s|$))", "", line)

        # Reszta linii to nazwa parku
        dzielnica = line.strip()

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


def create_lasy_df(txt_content):
    # Szukamy wzorca dla powierzchni lasów
    match = re.search(r'Informacja o powierzchni lasów w Krakowie: (\d+,\d+) ha', txt_content)

    if match:
        # Zamieniamy znalezioną powierzchnię na float, zamieniając przecinek na kropkę
        powierzchnia = float(match.group(1).replace(",", "."))

        # Tworzymy DataFrame z odpowiednimi kolumnami
        df = pd.DataFrame({
            'INDEX': [1],  # Stały indeks
            'MIASTO': ['Kraków'],  # Miasto: Kraków
            'POW (ha)': [powierzchnia]  # Powierzchnia lasów w ha
        })

        return df
    else:
        # Jeśli nie znajdziemy wzorca, zwracamy pusty DataFrame
        return pd.DataFrame(columns=['INDEX', 'MIASTO', 'POW (ha)'])


def create_parki_krak_df(dane_txt):
    # Podziel dane na linie
    lines = dane_txt.strip().split('\n')

    # Lista do przechowywania danych
    data = []

    # Przetwarzanie każdej linii
    for i, line in enumerate(lines, start=1):
        # Wyciągnięcie nazwy ulicy
        ulica_match = re.match(r'(.+?)\s*[-–]\s*', line)
        if ulica_match:
            ulica = ulica_match.group(1).strip()

        # Wyciągnięcie liczb (dodawanie drzew, jeśli jest więcej niż jedna liczba)
        liczby = re.findall(r'(\d+)\s*drzew', line)
        liczba_drzew = sum(map(int, liczby))  # Suma drzew

        # Dodajemy dane do listy
        data.append([i, ulica, liczba_drzew])

    # Tworzenie DataFrame
    df = pd.DataFrame(data, columns=['INDEX', 'ULICA', 'LICZBA_DRZEW'])

    return df


def read_txt_data(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def main():

    parki_pdf_file_path = "./green_data/Parki.pdf"
    parki_data = read_pdf_data(parki_pdf_file_path)
    parki_df = create_parki_df(parki_data)

    parki_kiesz_pdf_file_path = "./green_data/parki kieszonkowe 6.24.pdf"
    parki_kiesz_data = read_pdf_data(parki_kiesz_pdf_file_path)
    parki_kiesz_df = create_parki_df(parki_kiesz_data)


    lasy_txt_file_path = "./green_data/krakow_lasy.txt"
    lasy_data = read_txt_data(lasy_txt_file_path)
    lasy_df = create_lasy_df(lasy_data)

    parki_krako_txt_file_path = "./green_data/parki_krakowian.txt"
    parki_krak_data = read_txt_data(parki_krako_txt_file_path)
    parki_krak_df = create_parki_krak_df(parki_krak_data)


    print(parki_krak_df)


if __name__ == '__main__':
    main()




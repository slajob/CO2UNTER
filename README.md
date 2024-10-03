# ECO2COUNTER

ECO2COUNTER to aplikacja stworzona w ramach hackathonu HackYeah 2024. Jej celem jest pomoc użytkownikom w obliczaniu ich śladu węglowego na podstawie codziennych czynności. Ważnym elementem projektu był szczegółowy research dotyczący emisji generowanych przez różne aktywności oraz analiza miejsc zielonych w Krakowie, ich powierzchnia oraz zdolność pochłaniania dwutlenku węgla.

## Demo

Zdeployowaną wersję aplikacji można znaleźć pod adresem: [https://eco2counter.slajob.dev/](https://eco2counter.slajob.dev/)

## Opis

Projekt obejmuje:

- Obliczanie śladu węglowego na podstawie codziennych czynności takich jak podróże, zużycie energii w domu, jedzenie, itp.
- Szczegółowy research i analiza danych dotyczących emisji CO2 oraz miejsc zielonych w Krakowie
- Interaktywne narzędzie pozwalające użytkownikom na wprowadzanie danych i uzyskiwanie wyników w formie raportów

## Instalacja

Instrukcja instalacji lokalnej wersji aplikacji:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/slajob/eco2counter.git
   ```
2. Przejdź do katalogu z projektem:
   ```bash
   cd eco2counter
   ```
3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Uruchom lokalny serwer:
   ```bash
   python3 manage.py runserver 8000
   ```

Aplikacja powinna być dostępna pod adresem `http://localhost:8000`.

## Zespół

Autorzy:
- [slajob](https://github.com/slajob)
- [Skwarson96](https://github.com/Skwarson96)
- Klaudia Nitecka

## Linki

- Zgłoszone zadanie: [https://challengerocket.com/hackyeah-2024/works/eco2counter-e76f81#go-pagecontent](https://challengerocket.com/hackyeah-2024/works/eco2counter-e76f81#go-pagecontent)

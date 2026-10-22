import os
from json_funkcje import zapisz_json, odczytaj_json

FOLDER_GLOWNY = "dane"

def stworz_sciezki(krotki, folder=FOLDER_GLOWNY):
    "Zamienia krotki z main.py na ścieżki katalogów."

    sciezki = []
    for miesiac, dzien, pora in krotki:
        sciezka = os.path.join(folder, miesiac, dzien, pora)
        sciezki.append(sciezka)
    return sciezki

def stworz_pliki(sciezki):
    for sciezka in sciezki:
        os.makedirs(sciezka, exist_ok=True)
        zapisz_json(sciezka)

def zsumuj_dane(sciezki):
    suma = 0
    for sciezka in sciezki:
        suma += odczytaj_json(sciezka)
    return suma

def przetworz_sciezki(args):
    sciezki = stworz_sciezki(args.struktura_sciezek)

    if args.tworzenie:
        stworz_pliki(sciezki)
    else:
        suma = zsumuj_dane(sciezki)
        print(f"Suma czasu dla modelu A: {suma}s")
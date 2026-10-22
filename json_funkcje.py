import os
import json
import random

def zapisz_json(sciezka_katalogu):
    """
    Tworzy katalogi i zapisuje plik Dane.json z losowymi danymi.
    """
    sciezka_pliku = os.path.join(sciezka_katalogu, 'Dane.json')

    dane = {
        "Model": random.choice(['A', 'B', 'C']),
        "Wynik": random.randint(0, 1000),
        "Czas": f"{random.randint(0, 1000)}s"
    }

    try:
        with open(sciezka_pliku, 'w', encoding='utf-8') as f:
            json.dump(dane, f, indent=4)
        print(f"Utworzono plik: {sciezka_pliku}")
    except OSError as e:
        print(f"Nie można zapisać pliku w {sciezka_pliku}. Powód: {e}")


def odczytaj_json(sciezka_katalogu):
    """
    Odczytuje plik Dane.json i zwraca wartość int czasu dla model 'A'. W przeciwnym razie zwraca 0.
    """
    sciezka_pliku = os.path.join(sciezka_katalogu, 'Dane.json')

    if not os.path.exists(sciezka_pliku):
        print(f"Pomijam: Plik {sciezka_katalogu} nie istnieje.")
        return 0

    try:
        with open(sciezka_pliku, 'r', encoding='utf-8') as f:
            dane = json.load(f)

            if dane.get("Model") == "A":
                czas_str = dane.get("Czas", "0s")
                return int(czas_str.replace('s', ''))
    except PermissionError:
        print(f"Błąd: Brak uprawnień do odczytu pliku {sciezka_pliku}")
    except json.JSONDecodeError:
        print(f"Błąd: Plik {sciezka_pliku} nie jest poprawnym plikiem JSON.")
    except ValueError:
        print(f"Błąd: Wartość czasu w pliku {sciezka_pliku} jest nieprawidłowa.")

    return 0

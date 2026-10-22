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

    with open(sciezka_pliku, 'w', encoding='utf-8') as f:
        json.dump(dane, f, indent=4)
    print(f"Utworzono plik: {sciezka_pliku}")


def odczytaj_json(sciezka_katalogu):
    """
    Odczytuje plik Dane.json i zwraca wartość int czasu dla model 'A'. W przeciwnym razie zwraca 0.
    """
    sciezka_pliku = os.path.join(sciezka_katalogu, 'Dane.json')

    if not os.path.exists(sciezka_pliku):
        return 0

    try:
        with open(sciezka_pliku, 'r', encoding='utf-8') as f:
            dane = json.load(f)

            if dane.get("Model") == "A":
                czas_str = dane.get("Czas", "0s")
                return int(czas_str.replace('s', ''))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Błąd podczas odczytu pliku {sciezka_pliku}: {e}")

    return 0
import argparse
import unicodedata

DNI_MAP = {
    'pn': 'poniedziałek', 'poniedzialek': 'poniedziałek', 'poniedziałek': 'poniedziałek',
    'wt': 'wtorek', 'wtorek': 'wtorek',
    'sr': 'środa', 'śr': 'środa', 'sroda': 'środa', 'środa': 'środa',
    'cz': 'czwartek', 'czwartek': 'czwartek',
    'pt': 'piątek', 'piatek': 'piątek', 'piątek': 'piątek',
    'sb': 'sobota', 'sobota': 'sobota',
    'nd': 'niedziela', 'niedziela': 'niedziela'
}

DNI_KOLEJNOSC = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']

MIESIACE_DOZWOLONE = {
    'styczen', 'styczeń', 'luty', 'marzec', 'kwiecien', 'kwiecień', 'maj',
    'czerwiec', 'lipiec', 'sierpien', 'sierpień', 'wrzesien', 'wrzesień',
    'pazdziernik', 'październik', 'listopad', 'grudzien', 'grudzień'
}

def normalizuj(tekst):
    nfkd = unicodedata.normalize('NFKD', tekst)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

def rozwin_dni(z):
    z = normalizuj(z)
    if '-' in z:
        start, koniec = z.split('-', 1)
        p_start = DNI_MAP.get(start.strip())
        p_koniec = DNI_MAP.get(koniec.strip())
        if not p_start or not p_koniec:
            raise argparse.ArgumentTypeError(f"Nieznany skrót dnia: {z}")
        i1 = DNI_KOLEJNOSC.index(p_start)
        i2 = DNI_KOLEJNOSC.index(p_koniec)
        if i1 > i2:
            raise argparse.ArgumentTypeError(f"Błędny zakres dni: {z}")
        return DNI_KOLEJNOSC[i1:i2 + 1]
    else:
        p = DNI_MAP.get(z.strip())
        if not p:
            raise argparse.ArgumentTypeError(f"Nieznany dzień: {z}")
        return [p]

def normalizuj_miesiac(m):
    m_norm = normalizuj(m)
    if m_norm not in MIESIACE_DOZWOLONE:
        raise argparse.ArgumentTypeError(f"Nieobsługiwany miesiąc: {m}")
    mapping = {
        'styczen': 'styczeń', 'styczeń': 'styczeń',
        'luty': 'luty', 'marzec': 'marzec',
        'kwiecien': 'kwiecień', 'kwiecień': 'kwiecień',
        'maj': 'maj', 'czerwiec': 'czerwiec', 'lipiec': 'lipiec',
        'sierpien': 'sierpień', 'sierpień': 'sierpień',
        'wrzesien': 'wrzesień', 'wrześień': 'wrześień',
        'pazdziernik': 'październik', 'październik': 'październik',
        'listopad': 'listopad',
        'grudzien': 'grudzień', 'grudzień': 'grudzień'
    }
    return mapping.get(m_norm, m)

def pobierz_parametry():
    parser = argparse.ArgumentParser(
        description="Skrypt do obsługi danych w strukturze katalogów.",
        epilog="Przykład użycia: python main.py -m styczen luty -d pn-wt pt -p r w -t -c"
    )

    parser.add_argument("-m", "--miesiace", nargs="+", required=True, help="Miesiące")
    parser.add_argument("-d", "--dni", nargs="+", required=True, help="Zakresy dni (np. pn-wt)")
    parser.add_argument("-p", "--pory", nargs="*", default=[], choices=['r', 'w', 'rano', 'wieczor', 'wieczorem'], help="Pory dnia")

    # Wzajemnie wykluczające się opcje akcji
    g_akcja = parser.add_mutually_exclusive_group()
    g_akcja.add_argument("-t", "--tworzenie", action="store_true", help="Tworzenie plików")
    g_akcja.add_argument("-o", "--odczyt", action="store_true", help="Odczyt plików")

    # Wzajemnie wykluczające się opcje formatu
    g_fmt = parser.add_mutually_exclusive_group()
    g_fmt.add_argument("-c", "--csv", action="store_true", help="Format CSV")
    g_fmt.add_argument("-j", "--json", action="store_true", help="Format JSON")

    args = parser.parse_args()

    if len(args.miesiace) != len(args.dni):
        parser.error("Liczba miesięcy (-m) musi być równa liczbie zakresów dni (-d).")

    try:
        miesiace = [normalizuj_miesiac(m) for m in args.miesiace]
    except argparse.ArgumentTypeError as e:
        parser.error(str(e))

    sciezki = []
    for m, d_zakres in zip(miesiace, args.dni):
        try:
            dni = rozwin_dni(d_zakres)
        except argparse.ArgumentTypeError as e:
            parser.error(f"Miesiąc '{m}': {e}")
        for d in dni:
            sciezki.append((m, d))

    if len(args.pory) > len(sciezki):
        parser.error("Podano za dużo pór dnia w stosunku do liczby dni.")

    pory_koncowe = []
    for i, (m, d) in enumerate(sciezki):
        if i < len(args.pory):
            p_surowa = normalizuj(args.pory[i])
            pora = 'wieczorem' if p_surowa in ['w', 'wieczor', 'wieczorem'] else 'rano'
        else:
            pora = 'rano'
        pory_koncowe.append((m, d, pora))

    if not args.tworzenie and not args.odczyt:
        args.odczyt = True
    if not args.csv and not args.json:
        args.csv = True

    args.struktura_sciezek = pory_koncowe
    return args

def main():
    args = pobierz_parametry()
    
    # Przekazanie struktury do modułu Osoby 2:
    # przetworz_sciezki(args)

if __name__ == "__main__":
    main()
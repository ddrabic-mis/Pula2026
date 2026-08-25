"""Jednostavno trajno spremanje rezultata u JSON datoteku."""

import json
from pathlib import Path
from threading import Lock


BASE_DIR = Path(__file__).resolve().parent.parent
DATOTEKA = BASE_DIR / "data" / "rezultati.json"

# Zaštita od istodobnog čitanja i pisanja iste datoteke.
datoteka_lock = Lock()


def _ucitaj_bez_locka() -> list[dict]:
    """Interna funkcija; poziva se samo dok pozivatelj drži datoteka_lock."""

    if not DATOTEKA.exists():
        return []

    try:
        with DATOTEKA.open("r", encoding="utf-8") as datoteka:
            podaci = json.load(datoteka)
    except (json.JSONDecodeError, OSError):
        # Za edukacijsku aplikaciju vraćamo praznu listu ako je datoteka ručno
        # oštećena. U ozbiljnom sustavu pogrešku bismo dodatno evidentirali.
        return []

    return podaci if isinstance(podaci, list) else []


def ucitaj_rezultate() -> list[dict]:
    """Pretvara sadržaj JSON datoteke u Pythonovu listu rječnika."""

    with datoteka_lock:
        return _ucitaj_bez_locka()


def _spremi_bez_locka(rezultati: list[dict]) -> None:
    """Zapisuje cijelu listu u JSON; poziva se dok je lock aktivan."""

    DATOTEKA.parent.mkdir(parents=True, exist_ok=True)

    # Najprije pišemo u privremenu datoteku, a zatim je zamijenimo. Tako je puno
    # manja mogućnost da prekid programa ostavi napola zapisani JSON.
    privremena = DATOTEKA.with_suffix(".tmp")
    with privremena.open("w", encoding="utf-8") as datoteka:
        json.dump(rezultati, datoteka, ensure_ascii=False, indent=4)

    privremena.replace(DATOTEKA)


def dodaj_rezultat(rezultat: dict) -> None:
    """Učita postojeće zapise, doda novi i sve ponovno spremi."""

    with datoteka_lock:
        rezultati = _ucitaj_bez_locka()
        rezultati.append(rezultat)
        _spremi_bez_locka(rezultati)


def obrisi_rezultate() -> None:
    """Vraća datoteku rezultata na praznu JSON listu."""

    with datoteka_lock:
        _spremi_bez_locka([])


def izracunaj_ljestvicu(rezultati: list[dict]) -> list[dict]:
    """Iz liste pojedinačnih borbi računa statistiku svakog trenera."""

    treneri: dict[str, dict] = {}

    for rezultat in rezultati:
        trener = rezultat.get("trener", "Nepoznati trener")

        if trener not in treneri:
            treneri[trener] = {
                "trener": trener,
                "borbe": 0,
                "pobjede": 0,
                "porazi": 0,
            }

        zapis = treneri[trener]
        zapis["borbe"] += 1

        if rezultat.get("pobjednik") == "igrac":
            zapis["pobjede"] += 1
        else:
            zapis["porazi"] += 1

    ljestvica = list(treneri.values())

    for zapis in ljestvica:
        zapis["uspjesnost"] = round(
            zapis["pobjede"] / zapis["borbe"] * 100,
            1,
        )

    # Više pobjeda je važnije, zatim bolja uspješnost, pa ime radi stabilnog
    # poretka kada su prve dvije vrijednosti jednake.
    ljestvica.sort(
        key=lambda zapis: (
            -zapis["pobjede"],
            -zapis["uspjesnost"],
            zapis["trener"].lower(),
        )
    )

    for mjesto, zapis in enumerate(ljestvica, start=1):
        zapis["mjesto"] = mjesto

    return ljestvica

"""Dohvat i pretvaranje podataka iz vanjskog PokeAPI-ja."""

from functools import lru_cache

import requests


POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"


class PokeAPIError(Exception):
    """Naša pogreška kojom ostatku aplikacije opisujemo problem s PokeAPI-jem."""


@lru_cache(maxsize=64)
def dohvati_pokemona(ime: str) -> dict:
    """Dohvaća velik JSON i vraća samo podatke potrebne igri.

    Dekorator lru_cache pamti već dohvaćene Pokémone. Ponovna igra s Pikachuom
    zato ne mora ponovno čekati mrežni zahtjev dok aplikacija radi.
    """

    normalizirano_ime = ime.strip().lower()
    url = f"{POKEAPI_URL}/{normalizirano_ime}"

    try:
        odgovor = requests.get(url, timeout=8)
    except requests.RequestException as pogreska:
        raise PokeAPIError(
            "Nije moguće povezati se s PokeAPI-jem. Provjeri internetsku vezu."
        ) from pogreska

    if odgovor.status_code == 404:
        raise PokeAPIError(f"Pokémon '{ime}' nije pronađen.")

    try:
        odgovor.raise_for_status()
        podaci = odgovor.json()
    except (requests.RequestException, ValueError) as pogreska:
        raise PokeAPIError("PokeAPI je vratio neispravan odgovor.") from pogreska

    # Lista statistika iz PokeAPI-ja pretvara se u praktičan Pythonov rječnik.
    statistike = {
        zapis["stat"]["name"]: zapis["base_stat"]
        for zapis in podaci["stats"]
    }

    tipovi = [zapis["type"]["name"] for zapis in podaci["types"]]

    # Najprije pokušavamo uzeti veću ilustraciju. Ako je nema, koristimo mali
    # sprite. Izraz "or" vraća prvu vrijednost koja nije None/prazna.
    slika = (
        podaci["sprites"]["other"]["official-artwork"]["front_default"]
        or podaci["sprites"]["front_default"]
    )

    return {
        "id": podaci["id"],
        "ime": podaci["name"],
        "slika": slika,
        "tipovi": tipovi,
        "statistike": statistike,
    }

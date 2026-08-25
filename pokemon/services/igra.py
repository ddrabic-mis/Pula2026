"""Pravila, stanje i algoritmi potezne Pokémon igre."""

from datetime import datetime
import random
from uuid import uuid4

from services.pokeapi import dohvati_pokemona


# Ograničen popis ubrzava odabir i olakšava nastavniku pripremu zadataka.
# Slike na početnom ekranu dolaze iz javnog spremišta spriteova PokeAPI projekta.
POKEMONI = [
    {"ime": "bulbasaur", "id": 1},
    {"ime": "charmander", "id": 4},
    {"ime": "squirtle", "id": 7},
    {"ime": "pikachu", "id": 25},
    {"ime": "jigglypuff", "id": 39},
    {"ime": "meowth", "id": 52},
    {"ime": "psyduck", "id": 54},
    {"ime": "machop", "id": 66},
    {"ime": "geodude", "id": 74},
    {"ime": "gastly", "id": 92},
    {"ime": "eevee", "id": 133},
    {"ime": "snorlax", "id": 143},
]

DOZVOLJENI_POTEZI = {
    "brzi_napad",
    "snazni_napad",
    "obrana",
    "oporavak",
}

# Za jednostavniju igru koristimo samo prednosti. Pravi Pokémon sustav uključuje
# mnogo više odnosa i posebnih pravila, što učenici mogu dodati kao nadogradnju.
PREDNOSTI_TIPOVA = {
    "fire": {"grass", "bug", "ice", "steel"},
    "water": {"fire", "ground", "rock"},
    "grass": {"water", "ground", "rock"},
    "electric": {"water", "flying"},
    "ground": {"fire", "electric", "poison", "rock", "steel"},
    "rock": {"fire", "ice", "flying", "bug"},
    "ice": {"grass", "ground", "flying", "dragon"},
    "psychic": {"fighting", "poison"},
    "ghost": {"psychic", "ghost"},
    "dark": {"psychic", "ghost"},
    "fighting": {"normal", "ice", "rock", "dark", "steel"},
    "fairy": {"fighting", "dragon", "dark"},
    "flying": {"grass", "fighting", "bug"},
    "poison": {"grass", "fairy"},
    "bug": {"grass", "psychic", "dark"},
    "steel": {"ice", "rock", "fairy"},
    "dragon": {"dragon"},
}


def kreiraj_borca(podaci: dict) -> dict:
    """Od podataka PokeAPI-ja stvara promjenjivo stanje jednog borca."""

    statistike = podaci["statistike"]

    # Množenje osnovnog HP-a s 2 daje dovoljno duge, ali ne prespore borbe.
    maksimalni_hp = max(60, statistike["hp"] * 2)

    return {
        "ime": podaci["ime"],
        "slika": podaci["slika"],
        "tipovi": podaci["tipovi"],
        "hp": maksimalni_hp,
        "maksimalni_hp": maksimalni_hp,
        "napad": statistike["attack"],
        "obrana": statistike["defense"],
        "brzina": statistike["speed"],
        "brani_se": False,
        "preostali_oporavci": 2,
    }


def kreiraj_igru(trener: str, pokemon_igraca: str) -> dict:
    """Stvara potpuno početno stanje borbe."""

    dozvoljena_imena = {pokemon["ime"] for pokemon in POKEMONI}
    pokemon_igraca = pokemon_igraca.strip().lower()

    if pokemon_igraca not in dozvoljena_imena:
        raise ValueError("Odabrani Pokémon nije na popisu kamp-arene.")

    moguci_protivnici = list(dozvoljena_imena - {pokemon_igraca})
    ime_protivnika = random.choice(moguci_protivnici)

    igrac = kreiraj_borca(dohvati_pokemona(pokemon_igraca))
    racunalo = kreiraj_borca(dohvati_pokemona(ime_protivnika))

    return {
        "id": uuid4().hex[:8],
        "trener": trener,
        "igrac": igrac,
        "racunalo": racunalo,
        "runda": 0,
        "zavrsena": False,
        "pobjednik": None,
        "rezultat_spremljen": False,
        "povijest": [
            f"{trener} šalje {igrac['ime'].title()}a u arenu!",
            f"Računalo odgovara Pokémonom {racunalo['ime'].title()}!",
        ],
    }


def odaberi_potez_racunala(borac: dict, protivnik: dict) -> str:
    """Mala pravila umjetnog protivnika – nisu strojno učenje."""

    udio_hp = borac["hp"] / borac["maksimalni_hp"]

    # Ako je HP nizak, računalo često pokušava oporavak.
    if udio_hp < 0.35 and borac["preostali_oporavci"] > 0:
        if random.random() < 0.75:
            return "oporavak"

    # Ako protivnika može uskoro pobijediti, češće riskira snažan napad.
    if protivnik["hp"] < protivnik["maksimalni_hp"] * 0.25:
        return random.choice(["snazni_napad", "snazni_napad", "brzi_napad"])

    return random.choices(
        population=["brzi_napad", "snazni_napad", "obrana"],
        weights=[50, 35, 15],
        k=1,
    )[0]


def faktor_tipa(napadac: dict, branitelj: dict) -> float:
    """Vraća 1.5 ako primarni tip napadača ima prednost, inače 1.0."""

    tip_napadaca = napadac["tipovi"][0]
    ranjivi_tipovi = PREDNOSTI_TIPOVA.get(tip_napadaca, set())

    if any(tip in ranjivi_tipovi for tip in branitelj["tipovi"]):
        return 1.5

    return 1.0


def izvedi_potez(napadac: dict, branitelj: dict, potez: str) -> list[str]:
    """Mijenja stanje boraca i vraća rečenice za zapis borbe."""

    ime = napadac["ime"].title()
    protivnik = branitelj["ime"].title()

    if potez == "obrana":
        napadac["brani_se"] = True
        return [f"{ime} se priprema za obranu od sljedećeg napada."]

    if potez == "oporavak":
        if napadac["preostali_oporavci"] <= 0:
            return [f"{ime} više nema oporavaka i gubi potez."]

        prije = napadac["hp"]
        lijecenje = round(napadac["maksimalni_hp"] * 0.25)
        napadac["hp"] = min(napadac["maksimalni_hp"], prije + lijecenje)
        napadac["preostali_oporavci"] -= 1
        stvarno_lijecenje = napadac["hp"] - prije

        return [f"{ime} se oporavlja i vraća {stvarno_lijecenje} HP-a."]

    # Brzi je napad slabiji i precizniji; snažni je jači, ali češće promašuje.
    if potez == "brzi_napad":
        naziv_poteza = "brzi napad"
        jacina = 9
        preciznost = 0.95
    else:
        naziv_poteza = "snažni napad"
        jacina = 16
        preciznost = 0.70

    if random.random() > preciznost:
        return [f"{ime} koristi {naziv_poteza}, ali promašuje!"]

    tip_faktor = faktor_tipa(napadac, branitelj)
    slucajni_faktor = random.uniform(0.85, 1.0)

    steta = round(
        (napadac["napad"] / max(1, branitelj["obrana"]))
        * jacina
        * slucajni_faktor
        * tip_faktor
    )
    steta = max(2, steta)

    poruke = [f"{ime} koristi {naziv_poteza}."]

    if branitelj["brani_se"]:
        steta = max(1, round(steta * 0.5))
        branitelj["brani_se"] = False
        poruke.append(f"{protivnik} se brani i prepolavlja štetu.")

    branitelj["hp"] = max(0, branitelj["hp"] - steta)
    poruke.append(f"{protivnik} gubi {steta} HP-a.")

    if tip_faktor > 1:
        poruke.append("Prednost tipa pojačala je napad!")

    return poruke


def izvrsi_rundu(igra: dict, potez_igraca: str) -> None:
    """Izvršava oba poteza redom koji određuje brzina Pokémona."""

    igrac = igra["igrac"]
    racunalo = igra["racunalo"]
    potez_racunala = odaberi_potez_racunala(racunalo, igrac)

    igra["runda"] += 1
    igra["povijest"].append(f"--- Runda {igra['runda']} ---")

    # Svaki element trojke sadrži napadača, branitelja, odabrani potez i oznaku
    # strane. Ako je brzina jednaka, ždrijebamo tko prvi djeluje.
    akcija_igraca = (igrac, racunalo, potez_igraca, "igrac")
    akcija_racunala = (racunalo, igrac, potez_racunala, "racunalo")

    if igrac["brzina"] > racunalo["brzina"]:
        akcije = [akcija_igraca, akcija_racunala]
    elif racunalo["brzina"] > igrac["brzina"]:
        akcije = [akcija_racunala, akcija_igraca]
    else:
        akcije = [akcija_igraca, akcija_racunala]
        random.shuffle(akcije)

    for napadac, branitelj, potez, strana in akcije:
        # Ako je brži Pokémon već nokautirao sporijega, druga akcija se preskače.
        if napadac["hp"] <= 0:
            continue

        igra["povijest"].extend(izvedi_potez(napadac, branitelj, potez))

        if branitelj["hp"] <= 0:
            igra["zavrsena"] = True
            igra["pobjednik"] = strana
            igra["povijest"].append(
                f"{napadac['ime'].title()} pobjeđuje u borbi!"
            )
            break


def rezultat_zavrsene_igre(igra: dict) -> dict:
    """Od velikog stanja igre izdvaja mali zapis za rezultati.json."""

    pobjednicki_pokemon = (
        igra["igrac"]["ime"]
        if igra["pobjednik"] == "igrac"
        else igra["racunalo"]["ime"]
    )

    return {
        "id_igre": igra["id"],
        "vrijeme": datetime.now().isoformat(timespec="seconds"),
        "trener": igra["trener"],
        "pokemon_igraca": igra["igrac"]["ime"],
        "pokemon_racunala": igra["racunalo"]["ime"],
        "pobjednik": igra["pobjednik"],
        "pobjednicki_pokemon": pobjednicki_pokemon,
        "broj_rundi": igra["runda"],
    }

"""Glavna FastAPI aplikacija za igru Pokémon kamp-arena.

Ova je datoteka namjerno dovoljno mala da učenici mogu pratiti što radi
web-sloj aplikacije. Pravila igre nalaze se u services/igra.py, dohvat podataka
u services/pokeapi.py, a rad s JSON datotekom u services/spremiste.py.
"""

from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request

from services.igra import (
    DOZVOLJENI_POTEZI,
    POKEMONI,
    izvrsi_rundu,
    kreiraj_igru,
    rezultat_zavrsene_igre,
)
from services.pokeapi import PokeAPIError
from services.spremiste import (
    dodaj_rezultat,
    izracunaj_ljestvicu,
    obrisi_rezultate,
    ucitaj_rezultate,
)


# BASE_DIR je mapa u kojoj se nalazi main.py. Tako aplikacija ispravno pronalazi
# predloške i statičke datoteke čak i kada je pokrenemo iz neke druge mape.
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Pokémon kamp-arena",
    description="Edukacijska potezna igra izrađena u FastAPI-ju.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


# Aktivne igre čuvamo u memoriji. Ključ je jedinstveni ID igre, a vrijednost je
# rječnik sa stanjem igre. Gašenjem aplikacije aktivne igre nestaju, što je u
# ovom obrazovnom projektu namjerna i važna razlika u odnosu na JSON datoteku.
aktivne_igre: dict[str, dict] = {}

# FastAPI može istodobno obraditi više zahtjeva. Lock sprečava da dva zahtjeva
# u istom trenutku promijene istu igru. To nije baza podataka, nego mala zaštita
# zajedničke Pythonove strukture.
igre_lock = Lock()


class NovaIgraZahtjev(BaseModel):
    """JSON koji klijent šalje kada želi otvoriti novu igru."""

    trener: str = Field(min_length=1, max_length=30)
    pokemon: str = Field(min_length=1, max_length=30)


class PotezZahtjev(BaseModel):
    """JSON koji klijent šalje za odabrani potez."""

    potez: str


@app.get("/", response_class=HTMLResponse)
def pocetna_stranica(request: Request):
    """Vraća HTML sučelje igre, a ne JSON odgovor."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"pokemoni": POKEMONI},
    )


@app.get("/api/pokemoni")
def popis_pokemona():
    """Vraća manji, unaprijed odabrani popis Pokémona za kamp."""

    return {"pokemoni": POKEMONI}


@app.post("/api/igra", status_code=status.HTTP_201_CREATED)
def nova_igra(zahtjev: NovaIgraZahtjev):
    """Dohvaća Pokémone s PokeAPI-ja i otvara novu igru."""

    trener = zahtjev.trener.strip()
    if not trener:
        raise HTTPException(status_code=422, detail="Upiši ime trenera.")

    try:
        igra = kreiraj_igru(trener, zahtjev.pokemon)
    except ValueError as pogreska:
        raise HTTPException(status_code=400, detail=str(pogreska)) from pogreska
    except PokeAPIError as pogreska:
        raise HTTPException(status_code=503, detail=str(pogreska)) from pogreska

    with igre_lock:
        aktivne_igre[igra["id"]] = igra

    return igra


@app.get("/api/igra/{id_igre}")
def stanje_igre(id_igre: str):
    """Vraća trenutačno stanje jedne aktivne igre."""

    with igre_lock:
        igra = aktivne_igre.get(id_igre)

        if igra is None:
            raise HTTPException(status_code=404, detail="Igra nije pronađena.")

        return igra


@app.post("/api/igra/{id_igre}/potez")
def odigraj_potez(id_igre: str, zahtjev: PotezZahtjev):
    """Izvršava cijelu rundu: potez učenika i potez računala."""

    if zahtjev.potez not in DOZVOLJENI_POTEZI:
        raise HTTPException(
            status_code=400,
            detail=f"Nepoznat potez: {zahtjev.potez}",
        )

    with igre_lock:
        igra = aktivne_igre.get(id_igre)

        if igra is None:
            raise HTTPException(status_code=404, detail="Igra nije pronađena.")

        if igra["zavrsena"]:
            raise HTTPException(status_code=409, detail="Igra je već završena.")

        izvrsi_rundu(igra, zahtjev.potez)

        # Rezultat zapisujemo samo jednom, nakon prve runde koja završi igru.
        if igra["zavrsena"] and not igra["rezultat_spremljen"]:
            dodaj_rezultat(rezultat_zavrsene_igre(igra))
            igra["rezultat_spremljen"] = True

        return igra


@app.get("/api/rezultati")
def rezultati():
    """Vraća sve trajno spremljene rezultate borbi."""

    zapisi = ucitaj_rezultate()
    return {"broj_borbi": len(zapisi), "rezultati": zapisi}


@app.get("/api/ljestvica")
def ljestvica():
    """Iz rezultata u JSON-u računa poredak trenera."""

    return {"ljestvica": izracunaj_ljestvicu(ucitaj_rezultate())}


@app.delete("/api/rezultati")
def resetiraj_rezultate():
    """Briše povijest rezultata; korisničko sučelje traži potvrdu."""

    obrisi_rezultate()
    return {"poruka": "Svi rezultati su obrisani."}

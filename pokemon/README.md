# Pokémon kamp-arena

Potpuna edukacijska potezna igra za učenike koji već poznaju Python, osnovne
FastAPI rute i slanje GET zahtjeva bibliotekom `requests`.

## Što aplikacija radi

- učenik upisuje ime trenera i bira jednog od 12 Pokémona
- FastAPI s PokeAPI-ja dohvaća stvarne statistike i slike dvaju Pokémona
- računalni protivnik dobiva nasumičnog Pokémona i sam bira poteze
- brzina određuje redoslijed, napad i obrana određuju štetu
- napad može promašiti, obrana prepolavlja štetu, oporavak vraća HP
- prednost primarnog tipa povećava štetu
- aktivne igre čuvaju se u Pythonovu rječniku
- samo završeni rezultati spremaju se u `data/rezultati.json`
- iz JSON datoteke računa se ljestvica trenera

## Pokretanje na Windowsu

Otvorite terminal u mapi projekta i napravite virtualnu okolinu:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Ako naredba `py` nije dostupna, u prvoj naredbi upotrijebite `python`.

Zatim otvorite:

```text
http://127.0.0.1:8000
```

Automatska dokumentacija REST API-ja nalazi se na:

```text
http://127.0.0.1:8000/docs
```

## Struktura projekta

```text
pokemon_kamp_arena/
├── main.py                  FastAPI rute i aktivne igre
├── requirements.txt        potrebni Python paketi
├── data/
│   └── rezultati.json      trajno spremljene završene borbe
├── services/
│   ├── igra.py             pravila i algoritmi igre
│   ├── pokeapi.py          dohvat i obrada vanjskog JSON-a
│   └── spremiste.py        json.load i json.dump
├── static/
│   ├── app.js              HTTP komunikacija browsera i FastAPI-ja
│   └── style.css           izgled aplikacije
└── templates/
    └── index.html          HTML/Jinja2 korisničko sučelje
```

## Predloženi redoslijed poučavanja

1. Otvoriti `/docs` i ručno isprobati API rute.
2. U `pokeapi.py` analizirati razliku između `response.text` i `response.json()`.
3. Pratiti kako se veliki vanjski JSON pretvara u mali vlastiti rječnik.
4. Analizirati stanje jedne igre u rječniku `aktivne_igre`.
5. Predvidjeti rezultat funkcije za izračun štete prije pokretanja.
6. Istražiti kako JavaScriptov `fetch` šalje POST zahtjev.
7. Otvoriti `rezultati.json`, završiti borbu i ponovno pregledati datoteku.
8. Ugasiti aplikaciju: aktivna igra nestaje, završeni rezultati ostaju.

## Zadaci za učenike

### Osnovni

- dodati novog Pokémona u početni odabir
- promijeniti broj dopuštenih oporavaka
- prikazati napad, obranu i brzinu na karticama
- dodati broj poraza na ljestvicu

### Napredni

- uvesti otpornost tipova, a ne samo prednost
- spriječiti oporavak ako Pokémon već ima puni HP
- osmisliti uravnoteženiju formulu štete
- u JSON spremiti cijelu povijest završene borbe
- dodati filtar rezultata prema treneru ili Pokémonu

### Izazov

- omogućiti izbor tri Pokémona i izmjenu tijekom borbe
- izraditi nekoliko različitih strategija računalnog protivnika
- napisati simulaciju 1000 borbi i analizirati ravnotežu igre
- napraviti sobu s kodom za dvoboj dvaju učenika

## Važna ograničenja

Ovo je edukacijska aplikacija. Aktivne igre i rezultati nisu namijenjeni velikom
broju istodobnih korisnika ni pokretanju s više Uvicorn procesa. Za kamp, jednu
učionicu i lokalni razvoj JSON spremište je dovoljno jasno i praktično.

Za rad aplikacije potrebna je internetska veza jer podatke dohvaća s PokeAPI-ja.
Pokémon imena, statistike i slike vlasništvo su njihovih nositelja prava; projekt
je namijenjen poučavanju i demonstraciji.

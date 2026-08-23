# importiranje biblioteka Pythona
# fastapi - web framework za izgradnju API-ja
# uvicorn - ASGI server za pokretanje FastAPI aplikacija
import fastapi, uvicorn

app = fastapi.FastAPI()

# dekorator koji definira rutu za HTTP GET zahtjev na korijenskoj putanji ("/")
@app.get("/")
# on kaže da će funkcija koja slijedi biti izvršena kada se primi GET zahtjev na korijenskoj putanji
def korijen():
    return "Dobrodošli na korijensku putanju!"

# pokretanje FastAPI aplikacije pomoću uvicorn servera
# __name__ == "__main__" provjerava je li skripta pokrenuta izravno (a ne uvezena kao modul)
# __name__ je posebna varijabla u Pythonu koja sadrži ime trenutnog modula. 
# Kada se skripta pokrene izravno, __name__ će biti "__main__".
if __name__ == "__main__":
    # pokretanje uvicorn servera s aplikacijom, hostom i portom
    uvicorn.run(app, host="0.0.0.0", port=8000)
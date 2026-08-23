import fastapi
import random

app = fastapi.FastAPI()

# definiramo neki broj na početku
neki_broj: int = 0

def definiraj_novi_broj():
  global neki_broj
  neki_broj = random.randint(1, 9) # zamislimo neki broj između 1 i 9

#definiraj_novi_broj()

@app.get("/")
def pocetna():
    return "Aplikacija - POGODI BROJ"

@app.get("/broj/{broj}")
def pogodi_broj(broj: int):
    if broj>9 or broj<1:
        return "Broj koji ste unijeli nije između 1 i 9. Pokušajte ponovo."
    if neki_broj == broj:
        return f"Bravo! Pogodili ste broj {broj}!"
    elif broj < neki_broj:
        return f"Broj koji ste unijeli je manji od zamišljenog broja."
    else:
        return f"Broj koji ste unijeli je veći od zamišljenog broja."

@app.get("/broj")
def resetiraj_broj():
    # postavimo novi zamišljeni broj
    definiraj_novi_broj()
    return f"Zamišljeni broj je definiran. Pokušajte ga pogoditi!"

@app.get("/koji")
def koji_broj():
    return f"Zamišljeni broj je {neki_broj}."
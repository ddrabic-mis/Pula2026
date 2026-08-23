import fastapi, uvicorn
import random

app = fastapi.FastAPI()

a="INFORMATIKA"
boje=[
    "crvena",
    "plava",
    "zelena",
    "Žuta",
    "narančasta",
    "ljubičasta",
    "smeđa",
    "crna",
    "bijela"
]

@app.get("/")
def pocetna():
    #return f"Danas sam zamislio broj {random.randint(1, 100)}"
    #return f"iz rijači {a} sam zamislio slovo {random.choice(a)}"
    i=random.randint(0, len(a)-1)
    return f"iz rijači {a} sam zamislio slovo {a[i]} na indexu {i}"

@app.get("/boja")
def boja():
    moja_boja = random.choice(boje) # izaberemo neku boju iz liste boja
    return f"Boja koju sam zamislio je {moja_boja.upper()}" # vratimo boju u velikim slovima
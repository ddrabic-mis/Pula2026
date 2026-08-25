import fastapi
import json
#import zivotinje_popis
#import zivotinje_popis as z
from zivotinje_popis import zivotinje

app = fastapi.FastAPI()

@app.get("/")
def root():
    return "Aplikacija o ŽIVOTINJAMA"

@app.get("/zivotinje")
def get_zivotinje():
    rez=[]
    for zivotinja in zivotinje:
        rez.append(zivotinja['vrsta'])
    # json.dump pretvara iz Python strukture u STRING kako bi je mogla prenijeti putem interneta
    return json.dumps(rez, ensure_ascii=False)

@app.get("/sve")
def sav_sadrzaj():
    return json.dumps(zivotinje, ensure_ascii=False)
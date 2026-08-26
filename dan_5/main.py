# uključuejmo fastapi biblioteku i iz nje FastAPI i Request
from fastapi import FastAPI, Request
# uključuejmo Jinja2Templates iz fastapi biblioteke za rad s predlošcima
from fastapi.templating import Jinja2Templates
# uključuejmo Response iz fastapi.responses za vraćanje HTML odgovora
from fastapi.responses import HTMLResponse

from data.podaci import *
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def pocetna(request: Request):
    osoba = random.choice(osobe)
    boja= random.choice(boje)
    fsize=random.randint(24, 256)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            'ime': osoba['ime'],
            'mjesto': osoba['mjesto'],
            'boja': boja,
            'velicina': fsize
            },
        )

@app.get("/about", response_class=HTMLResponse)
def o_nama(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            },
        )
# tik-tak-toe igra
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

igra_aktivna = True # igra je aktivna
krizic=True
pobjednik=None

def init():
  global igra_aktivna, krizic, pobjednik
  # početak igre
  igra_aktivna = True
  krizic=True
  pobjednik=None
  return [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]

# pamtiti ćemo rezultat u memoriji - matrici 3x3
polje=init() # postavili smo početnu matricu

def odredi_pobjednika():
  global polje
  # po redovima
  for i in range(3):
    redak="".join([str(x) for x in polje[i]])
    if "111" in redak:
      return "X"
    if "222" in redak:
      return "O"
  # po stupcima
  for j in range(3):
    stupac="".join([str(polje[i][j]) for i in range(3)])
    if "111" in stupac:
      return "X"
    if "222" in stupac:
      return "O"
  # po dijagonalama
  dijagonala1="".join([str(polje[i][i]) for i in range(3)])
  dijagonala2="".join([str(polje[i][2-i]) for i in range(3)])
  if "111" in dijagonala1 or "111" in dijagonala2:
    return "X"
  if "222" in dijagonala1 or "222" in dijagonala2:
    return "O"
  return None

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
       request=request,
       name="index.html",
       context={
          "polje": polje, 
          "aktivna": igra_aktivna,
          "krizic": krizic,
          "pobjednik": pobjednik
          }
       )

@app.post("/nova_igra", response_class=HTMLResponse)
def nova_igra(request: Request):
    global polje
    polje=init() # postavili smo početnu matricu
    # redirect na početnu stranicu
    return RedirectResponse(url="/", status_code=303) 

@app.get("/potez/{i}/{j}/{igrac_krizic}", response_class=HTMLResponse)
def potez(request: Request, i: int, j: int, igrac_krizic: bool):
    global polje, igra_aktivna, pobjednik, krizic
    if not igra_aktivna:
        return RedirectResponse(url="/", status_code=303) 
    if polje[i][j] != 0:
        return RedirectResponse(url="/", status_code=303) 
    # odigrali smo potez
    polje[i][j] = 1 if igrac_krizic else 2
    # provjeriti je li netko pobijedio
    pobjednik = odredi_pobjednika()
    if pobjednik:
        igra_aktivna = False
    else:
        # promijeniti igrača
        krizic = not krizic
    return RedirectResponse(url="/", status_code=303)
# tik-tak-toe igra
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="tik-tak-toe-tajni-kljuc")
templates = Jinja2Templates(directory="templates")

def init(request: Request):
  # početak igre
  request.session["igra_aktivna"] = True
  request.session["krizic"] = True
  request.session["pobjednik"] = None
  request.session["polje"] = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]

def odredi_pobjednika(polje):
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
    if "polje" not in request.session:
       init(request)
    return templates.TemplateResponse(
       request=request,
       name="index.html",
       context={
          "polje": request.session["polje"],
          "aktivna": request.session["igra_aktivna"],
          "krizic": request.session["krizic"],
          "pobjednik": request.session["pobjednik"]
          }
       )

@app.post("/nova_igra", response_class=HTMLResponse)
def nova_igra(request: Request):
    init(request) # postavili smo početnu matricu
    # redirect na početnu stranicu
    return RedirectResponse(url="/", status_code=303)

@app.get("/potez/{i}/{j}/{igrac_krizic}", response_class=HTMLResponse)
def potez(request: Request, i: int, j: int, igrac_krizic: bool):
    if "polje" not in request.session:
        init(request)
    polje = request.session["polje"]
    igra_aktivna = request.session["igra_aktivna"]
    if not igra_aktivna:
        return RedirectResponse(url="/", status_code=303)
    if polje[i][j] != 0:
        return RedirectResponse(url="/", status_code=303)
    # odigrali smo potez
    polje[i][j] = 1 if igrac_krizic else 2
    # provjeriti je li netko pobijedio
    pobjednik = odredi_pobjednika(polje)
    request.session["polje"] = polje
    request.session["pobjednik"] = pobjednik
    if pobjednik:
        request.session["igra_aktivna"] = False
    else:
        # promijeniti igrača
        request.session["krizic"] = not request.session["krizic"]
    return RedirectResponse(url="/", status_code=303)

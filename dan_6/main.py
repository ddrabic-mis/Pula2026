# tik-tak-toe igra
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

igra_aktivna = True # igra je aktivna
krizic=True

def init():
  global igra_aktivna, krizic
  # početak igre
  igra_aktivna = True
  krizic=True
  return [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]

# pamtiti ćemo rezultat u memoriji - matrici 3x3
polje=init() # postavili smo početnu matricu



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
       request=request,
       name="index.html",
       context={
          "polje": polje, 
          "aktivna": igra_aktivna,
          "krizic": krizic
          }
       )

@app.post("/nova_igra", response_class=HTMLResponse)
def nova_igra(request: Request):
    global polje
    polje=init() # postavili smo početnu matricu
    # redirect na početnu stranicu
    return RedirectResponse(url="/", status_code=303) 
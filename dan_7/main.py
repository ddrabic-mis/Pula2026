# tik-tak-toe igra
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

app=FastAPI()
templates=Jinja2Templates(directory="templates")

poruke=[]

@app.get("/", response_class=HTMLResponse)
def pocetna(request:Request):
  return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
      'poruke':poruke
    }
  )

@app.get("/posalji/{ime}/{poruka}", response_class=HTMLResponse)
def posalji(request:Request, ime:str, poruka:str):
  # ažuriraj poruke
  print(ime, poruka)
  poruke.append({ime:poruka})
  return RedirectResponse(url="/", status_code=303)
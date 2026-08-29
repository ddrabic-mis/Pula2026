# tik-tak-toe igra
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import datetime

app=FastAPI()
templates=Jinja2Templates(directory="templates")
# definiranje mape gdje će se nalaziti statičke datoteke projekta
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="poruke-igra-123")

poruke=[]

@app.get("/", response_class=HTMLResponse)
def pocetna(request:Request):
  return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
      'poruke':poruke,
      'nadimak':request.session.get('nadimak','')
    }
  )

@app.get("/posalji/{ime}/{poruka}", response_class=HTMLResponse)
def posalji(request:Request, ime:str, poruka:str):
  # ažuriraj poruke
  print(ime, poruka)
  if not request.session.get('nadimak'):
    request.session["nadimak"]=ime
  poruke.append( (f"{datetime.datetime.now():%d.%m.%Y. %H:%M:%S}", ime, poruka) )
  return RedirectResponse(url="/", status_code=303)
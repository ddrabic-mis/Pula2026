from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()
templates=Jinja2Templates(directory="templates")
# definiranje mape gdje će se nalaziti statičke datoteke projekta
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret-key-random1231233")

import services

pogreska=0

@app.get('/', response_class=HTMLResponse)
def pocetak(request:Request):
  return templates.TemplateResponse(
    request=request,
    name='index.html',
    context={

    }
  )
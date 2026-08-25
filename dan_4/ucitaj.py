import requests
import json
# JSON = Javascript Object Notation
# struktura podataka koja se koristi za razmjenu podataka 
# između servera i klijenta
# slična je Pythonovim rječnicima i listama

def popis_vrsti():
  response = requests.get('http://10.112.0.20:8000/zivotinje')
  if response.status_code == 200:
    # imamo ispravne podatke
    print(response.text) # response kao tekst - string
    a=response.json() # response koji ima string vrijednost JSON-a
    print(a[0])
    print(type(a)) # ovo je string
    b=json.loads(a) # pretvaramo JSNO string u Pythonov objekt
    print(type(b)) # ovo je lista
  else:
    # došlo je do greške
    print(f"Greška: {response.status_code}")

def sve_zovitinje():
  response = requests.get('http://10.112.0.20:8000/sve')
  if response.status_code==200:
    # pretvaramo u Python strukture
    obj=response.json()
    print(type(obj))
    print(obj)

# izbornik
while True:
  izbor=input(
'''
IZBORNIK
-----------------------------
1. popis svih vrsti životinja
2. podaci svih životinja
IZLAZ
''')
  match izbor:
    case "1": popis_vrsti()
    case "2": sve_zovitinje()
    case _:
      exit()
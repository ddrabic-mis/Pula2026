import requests
from pprint import pprint

url='https://api.dictionaryapi.dev/api/v2/entries/en/'

def obradi(rijec):
  # dohvaćamo podatke
  res=requests.get(f"{url}{rijec}")
  if res.status_code==200:
    # pretvorimo JSON string u Python objekt - strukturu
    podaci=res.json() # pretvorili smo iz JSON u Python strukturu
    #print(type(podaci))
    dio1=podaci[0]
    print(dio1)
    pprint(dio1['phonetics'])
    pprint(dio1['meanings'])

while True:
  r=input("Unesei riječ: ")
  if not r:
    break
  obradi(r)
import requests

odgovor = requests.get("http://10.112.0.20:8000/koji")
print(odgovor.text)

a,b=map(int, input("Unesite dva broja za zbrajanje (odvojena razmakom): ").split())
odgovor = requests.get(f"http://10.112.0.20:8000/zbroji/{a}/{b}")
print(odgovor.text)
import requests # biblioteka za HTTP zahtjeve

def unos_imena():
  while True:
      ime = input("Unesite ime učenika (ili ništa za završetak): ")
      if not ime:
          break
      # slanje GET zahtjeva na FastAPI aplikaciju za dodavanje imena
      odgovor = requests.get(f"http://10.112.0.20:8000/ime/{ime}")
      # ispis odgovora s FastAPI aplikacije
      print(odgovor.text)
      print(f"{odgovor.status_code} - {odgovor.reason}")
      print(f"{odgovor.url=}")

def dohvati_imena():
    # slanje GET zahtjeva na FastAPI aplikaciju za dohvat svih imena
    odgovor = requests.get("http://10.112.0.20:8000/imena")
    # ispis odgovora s FastAPI aplikacije
    print(odgovor.text)

def izbornik():
    while True:
        print("\nIzbornik:")
        print("1. Unos imena učenika")
        print("2. Dohvat svih imena učenika")
        print("3. Izlaz")
        izbor = input("Odaberite opciju (1-3): ")

        if izbor == "1":
            unos_imena()
        elif izbor == "2":
            dohvati_imena()
        else:
            print("Izlaz iz programa.")
            break

izbornik()
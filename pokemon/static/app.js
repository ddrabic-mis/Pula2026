// JavaScript je klijent aplikacije: reagira na klikove, šalje HTTP zahtjeve
// FastAPI-ju i primljeni JSON pretvara u promjene HTML stranice.

let odabraniPokemon = null;
let idIgre = null;
let brojPrikazanihPoruka = 0;

const odabirSekcija = document.querySelector("#odabir");
const arenaSekcija = document.querySelector("#arena");
const pokreniGumb = document.querySelector("#pokreni-igru");
const poruka = document.querySelector("#odabir-poruka");
const potezi = document.querySelector("#potezi");


// Klik na karticu pamti odabir i vizualno označava samo jednu karticu.
document.querySelectorAll(".pokemon-choice").forEach((gumb) => {
    gumb.addEventListener("click", () => {
        document.querySelectorAll(".pokemon-choice").forEach((kartica) => {
            kartica.classList.remove("selected");
        });

        gumb.classList.add("selected");
        odabraniPokemon = gumb.dataset.pokemon;
        pokreniGumb.disabled = false;
        poruka.textContent = `Odabran je ${formatirajIme(odabraniPokemon)}.`;
    });
});


pokreniGumb.addEventListener("click", async () => {
    const trener = document.querySelector("#trener").value.trim();

    if (!trener) {
        poruka.textContent = "Najprije upiši ime trenera.";
        document.querySelector("#trener").focus();
        return;
    }

    promijeniZauzetost(pokreniGumb, true, "Dohvaćam Pokémone...");
    poruka.textContent = "FastAPI dohvaća podatke s PokeAPI-ja.";

    try {
        const igra = await posaljiJSON("/api/igra", {
            method: "POST",
            body: JSON.stringify({ trener, pokemon: odabraniPokemon }),
        });

        idIgre = igra.id;
        brojPrikazanihPoruka = 0;
        odabirSekcija.classList.add("hidden");
        arenaSekcija.classList.remove("hidden");
        prikaziIgru(igra);
    } catch (pogreska) {
        poruka.textContent = pogreska.message;
    } finally {
        promijeniZauzetost(pokreniGumb, false, "Pokreni borbu");
    }
});


document.querySelectorAll("[data-potez]").forEach((gumb) => {
    gumb.addEventListener("click", async () => {
        if (!idIgre) return;

        onemoguciPoteze(true);

        try {
            const igra = await posaljiJSON(`/api/igra/${idIgre}/potez`, {
                method: "POST",
                body: JSON.stringify({ potez: gumb.dataset.potez }),
            });

            prikaziIgru(igra);
        } catch (pogreska) {
            alert(pogreska.message);
        } finally {
            // Kod završene igre prikaziIgru skriva cijelo područje poteza.
            if (!potezi.classList.contains("hidden")) {
                onemoguciPoteze(false);
            }
        }
    });
});


function prikaziIgru(igra) {
    prikaziBorca("igrac", igra.igrac);
    prikaziBorca("racunalo", igra.racunalo);

    document.querySelector("#runda").textContent = `Runda ${igra.runda}`;
    document.querySelector("#oporavak-tekst").textContent =
        `Vraća 25% HP-a • preostalo ${igra.igrac.preostali_oporavci}`;

    const dnevnik = document.querySelector("#povijest");

    // Dodajemo samo nove poruke kako se stari elementi ne bi svaki put stvarali.
    igra.povijest.slice(brojPrikazanihPoruka).forEach((tekst) => {
        const redak = document.createElement("p");
        redak.textContent = tekst;

        if (tekst.startsWith("---")) redak.classList.add("round-line");
        if (tekst.includes("pobjeđuje")) redak.classList.add("winner-line");

        dnevnik.appendChild(redak);
    });

    brojPrikazanihPoruka = igra.povijest.length;
    dnevnik.scrollTop = dnevnik.scrollHeight;

    if (igra.zavrsena) {
        potezi.classList.add("hidden");
        document.querySelector("#zavrsni-ekran").classList.remove("hidden");

        document.querySelector("#zavrsna-poruka").textContent =
            igra.pobjednik === "igrac"
                ? `Pobjeda! ${formatirajIme(igra.igrac.ime)} osvaja arenu.`
                : `${formatirajIme(igra.racunalo.ime)} je ovaj put pobijedio.`;
    }
}


function prikaziBorca(prefiks, borac) {
    document.querySelector(`#${prefiks}-ime`).textContent = formatirajIme(borac.ime);
    document.querySelector(`#${prefiks}-slika`).src = borac.slika;
    document.querySelector(`#${prefiks}-hp-tekst`).textContent =
        `${borac.hp} / ${borac.maksimalni_hp}`;

    const postotak = Math.max(0, borac.hp / borac.maksimalni_hp * 100);
    const hpTraka = document.querySelector(`#${prefiks}-hp`);
    hpTraka.style.width = `${postotak}%`;
    hpTraka.classList.toggle("low", postotak <= 30);

    const tipovi = document.querySelector(`#${prefiks}-tipovi`);
    tipovi.replaceChildren();

    borac.tipovi.forEach((tip) => {
        const oznaka = document.createElement("span");
        oznaka.className = `type type-${tip}`;
        oznaka.textContent = tip;
        tipovi.appendChild(oznaka);
    });
}


document.querySelector("#nova-igra").addEventListener("click", () => {
    window.location.reload();
});


const dialog = document.querySelector("#ljestvica-dialog");

document.querySelector("#otvori-ljestvicu").addEventListener("click", async () => {
    dialog.showModal();
    await ucitajLjestvicu();
});

document.querySelector("#zatvori-ljestvicu").addEventListener("click", () => {
    dialog.close();
});

document.querySelector("#obrisi-rezultate").addEventListener("click", async () => {
    if (!confirm("Želiš li zaista obrisati sve spremljene rezultate?")) return;

    try {
        await posaljiJSON("/api/rezultati", { method: "DELETE" });
        await ucitajLjestvicu();
    } catch (pogreska) {
        alert(pogreska.message);
    }
});


async function ucitajLjestvicu() {
    const sadrzaj = document.querySelector("#ljestvica-sadrzaj");
    sadrzaj.textContent = "Učitavam...";

    try {
        const podaci = await posaljiJSON("/api/ljestvica");

        if (podaci.ljestvica.length === 0) {
            sadrzaj.innerHTML = "<p>Još nema završenih borbi.</p>";
            return;
        }

        const tablica = document.createElement("table");
        tablica.innerHTML = `
            <thead>
                <tr><th>#</th><th>Trener</th><th>Mečevi</th><th>Pobjede</th><th>Uspješnost</th></tr>
            </thead>
            <tbody></tbody>
        `;

        const tijelo = tablica.querySelector("tbody");

        podaci.ljestvica.forEach((zapis) => {
            const red = document.createElement("tr");
            red.innerHTML = `
                <td>${zapis.mjesto}</td>
                <td>${siguranTekst(zapis.trener)}</td>
                <td>${zapis.borbe}</td>
                <td>${zapis.pobjede}</td>
                <td>${zapis.uspjesnost}%</td>
            `;
            tijelo.appendChild(red);
        });

        sadrzaj.replaceChildren(tablica);
    } catch (pogreska) {
        sadrzaj.textContent = pogreska.message;
    }
}


async function posaljiJSON(url, opcije = {}) {
    const odgovor = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...opcije,
    });

    const podaci = await odgovor.json();

    if (!odgovor.ok) {
        throw new Error(podaci.detail || "Dogodila se pogreška.");
    }

    return podaci;
}


function onemoguciPoteze(da) {
    document.querySelectorAll("[data-potez]").forEach((gumb) => {
        gumb.disabled = da;
    });
}


function promijeniZauzetost(gumb, zauzet, tekst) {
    gumb.disabled = zauzet;
    gumb.textContent = tekst;
}


function formatirajIme(ime) {
    return ime.charAt(0).toUpperCase() + ime.slice(1);
}


function siguranTekst(tekst) {
    const element = document.createElement("span");
    element.textContent = tekst;
    return element.innerHTML;
}

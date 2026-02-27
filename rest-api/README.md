# REST API – Opgave 1

**Kursus:** Softwaresikkerhed
**Institution:** Zealand Næstved

---

## Formål

Formålet med denne opgave er at udvikle et REST API i Python ved brug af FastAPI.
API'et skal understøtte grundlæggende CRUD-funktionalitet og demonstrere forståelse for:

- REST-principper
- HTTP-metoder
- Datahåndtering
- Lagdelt arkitektur
- Fejlhåndtering

Systemet anvender en flat-file database (JSON) som datalager.

---

## Arkitektur

Løsningen er opdelt i følgende lag:

| Lag | Fil | Ansvar |
|-----|-----|--------|
| API-lag | `main.py` | Håndterer HTTP-requests og eksponerer endpoints |
| Model-lag | `models.py` | Definerer datatyper ved brug af Pydantic |
| Data-lag | `flat_file_loader.py` | Ansvarlig for læsning og skrivning til JSON-filen |
| Database | `db/users.json` | Flat-file database med brugerdata |

Denne opdeling sikrer separation of concerns og gør løsningen mere overskuelig og vedligeholdbar.

---

## Datamodel

Brugerobjektet består af følgende felter:

| Felt | Type | Beskrivelse |
|------|------|-------------|
| `person_id` | `int` | Unik identifikator |
| `first_name` | `str` | Fornavn |
| `last_name` | `str` | Efternavn |
| `address` | `str` | Adresse |
| `street_number` | `str` | Husnummer |
| `password` | `str` | Adgangskode |
| `enabled` | `bool` | Om brugeren er aktiv |

Datamodellen valideres automatisk via Pydantic.

---

## Endpoints

### `POST /users`
Opretter en ny bruger.

- Hvis `person_id` allerede eksisterer, returneres `HTTP 400`
- **Risici:** Dubletter eller inkonsistent data kan opstå ved fejl

### `GET /users/{person_id}`
Returnerer en specifik bruger.

- Hvis brugeren ikke findes, returneres `HTTP 404`
- **Risici:** Systemet kan returnere forkert bruger eller håndtere manglende brugere ukorrekt

### `PUT /users/{person_id}`
Opdaterer en eksisterende bruger.

- Hvis brugeren ikke findes, returneres `HTTP 404`
- **Risici:** Eksisterende data kan overskrives forkert, eller ændringer gemmes ikke korrekt

### `DELETE /users/{person_id}`
Sletter en bruger fra systemet.

- Hvis brugeren ikke findes, returneres `HTTP 404`
- **Risici:** Brugere kan forblive i systemet, eller uautoriseret sletning kan ske ved manglende kontrol

### `GET /users`
Returnerer en liste over alle brugere.

- **Risici:** Tom liste returneres selvom data eksisterer, eller forkert datastruktur returneres

---

## REST-principper

API'et følger standard REST-principper:

| Metode | Formål |
|--------|--------|
| `POST` | Oprettelse |
| `GET` | Læsning |
| `PUT` | Opdatering |
| `DELETE` | Sletning |

Derudover anvendes ressourcebaseret routing og korrekte HTTP-statuskoder.

---

## Databehandling

Data gemmes i en JSON-fil. Ved hver operation:

1. Data læses fra fil
2. Operation udføres i memory
3. Data gemmes tilbage i filen

**Fordele:**
- Simpelt setup
- Ingen ekstern database nødvendig
- Velegnet til små systemer eller testmiljøer

**Begrænsninger:**
- Ingen concurrency-håndtering
- Ikke egnet til større produktion
- Ingen transaktionsstyring

---

## Fejlhåndtering

API'et anvender `HTTPException` for at returnere:

| Statuskode | Betydning |
|------------|-----------|
| `400 Bad Request` | Dublet ved oprettelse |
| `404 Not Found` | Bruger ikke fundet |

Dette sikrer korrekt REST-adfærd og tydelig fejlhåndtering.

---

## Kørsel

Fra mappen `rest-api`:

```bash
python -m uvicorn src.main:app --reload
```

Swagger-dokumentation kan herefter tilgås via:

```
http://127.0.0.1:8000/docs
```

---

## Konklusion

Løsningen demonstrerer:

- Implementering af REST API i FastAPI
- CRUD-funktionalitet
- Strukturering i lag
- Brug af Pydantic til validering
- Korrekt brug af HTTP-statuskoder
- Flat-file datalagring

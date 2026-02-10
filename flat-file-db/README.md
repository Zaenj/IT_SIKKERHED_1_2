# Flat File Database

**Opgave:** Flat file database med JSON
**Kursus:** Softwaresikkerhed — Zealand Næstved

---

## Hvorfor en flat-file database?

En flat-file database (bare en JSON-fil) kan give mening når man ikke har brug for en rigtig database:

- Man behøver ikke installere MySQL, PostgreSQL eller lignende — filen kan bare køre direkte.
- Data kan åbnes i en teksteditor, så det er nemt at tjekke hvad der er gemt.
- Til prototyper og undervisning er det fint, fordi man kan fokusere på selve logikken.
- Filen kan kopieres mellem systemer uden problemer.

Det skalerer selvfølgelig ikke til mange brugere på én gang, og der er ingen transaktionssikkerhed — men til denne opgave er det fint nok.

---

## Understøttede funktioner

| Funktion | Beskrivelse |
|----------|-------------|
| `create_user(...)` | Opretter en ny bruger og gemmer i `db/users.json`. Fejler hvis `person_id` allerede findes. |
| `read_user(person_id)` | Læser en bruger ud fra `person_id`. Returnerer `None` hvis brugeren ikke findes. |
| `update_user(person_id, **fields)` | Opdaterer en eller flere felter på en eksisterende bruger. |
| `enable_user(person_id)` | Sætter brugerens `enabled` felt til `True`. |
| `disable_user(person_id)` | Sætter brugerens `enabled` felt til `False`. |

### User schema

```json
{
  "person_id": "1",
  "first_name": "Anders",
  "last_name": "Jensen",
  "address": "Parkvej",
  "street_number": "12",
  "password": "hemmeligt123",
  "enabled": true
}
```

---

## Testdesign-teknikker

Testene bruger følgende teknikker:

- **Ækvivalenspartitionering** — vi tester både med gyldige data (opretter en bruger normalt) og ugyldige data (prøver at oprette en duplikat).
- **Grænseværdianalyse** — f.eks. at læse en bruger der ikke findes, og tjekke at vi får `None` tilbage.
- **Given / When / Then** — alle tests følger den struktur, så det er tydeligt hvad der testes.

---

## Tests og funktionalitet

### Test 1: `test_create_user`
- **Given:** En tom database
- **When:** En ny bruger oprettes med gyldige data
- **Then:** Brugeren gemmes og kan læses tilbage
- **Risiko hvis testen fejler:** Hvis brugere ikke kan oprettes, virker resten af systemet heller ikke.

### Test 2: `test_create_duplicate_user_raises_error`
- **Given:** En bruger med person_id '1' eksisterer allerede
- **When:** Vi forsøger at oprette en ny bruger med samme person_id
- **Then:** En `ValueError` kastes
- **Risiko hvis testen fejler:** Man kan ende med duplikerede brugere i databasen, og så ved man ikke hvilken der er den rigtige.

### Test 3: `test_read_nonexistent_user_returns_none`
- **Given:** En tom database
- **When:** Vi forsøger at læse en bruger der ikke findes
- **Then:** `None` returneres
- **Risiko hvis testen fejler:** Programmet kan crashe hvis man slår en bruger op der ikke findes.

### Test 4: `test_update_user`
- **Given:** En bruger eksisterer i databasen
- **When:** Vi opdaterer brugerens adresse
- **Then:** Den nye adresse er gemt korrekt
- **Risiko hvis testen fejler:** Brugere sidder fast med gammel data der ikke kan rettes.

### Test 5: `test_disable_user`
- **Given:** En aktiv bruger eksisterer
- **When:** Vi deaktiverer brugeren
- **Then:** Brugerens `enabled` felt er `False`
- **Risiko hvis testen fejler:** Kompromitterede konti kan ikke lukkes ned, hvilket er en sikkerhedsrisiko.

### Test 6: `test_enable_user`
- **Given:** En deaktiveret bruger eksisterer
- **When:** Vi aktiverer brugeren
- **Then:** Brugerens `enabled` felt er `True`
- **Risiko hvis testen fejler:** En bruger der er blevet deaktiveret kan ikke komme ind igen.

### Test 7: `test_password_is_hashed__expected_fail` (FEJLER MED VILJE)
- **Given:** En bruger oprettes med et plaintext password
- **When:** Vi læser brugeren fra databasen
- **Then:** Det gemte password burde IKKE matche plaintext — men det gør det, fordi hashing ikke er implementeret
- **Risiko hvis testen fejler:** Passwords ligger i klartekst i JSON-filen — det er en alvorlig sikkerhedsrisiko.
- **Hvad skal ændres:** Man skal tilføje password-hashing (f.eks. bcrypt) i `create_user()`.

### Test 8: `test_delete_user` (SKIPPED)
- **Given:** En bruger eksisterer
- **When:** Vi sletter brugeren
- **Then:** Brugeren kan ikke længere findes
- **Hvorfor skipped:** `delete_user()` findes ikke endnu i koden.
- **Hvad skal ændres:** Skriv en `delete_user(person_id)` funktion i `flat_file_db.py`.

---

## Kør tests

```bash
cd flat-file-db
python -m pytest tests/ -v
```

---

## Test execution (screenshots)

### Beståede tests

<img width="1270" height="296" alt="Passed" src="https://github.com/user-attachments/assets/d17168dd-b806-4a02-a4dc-4bccdde77e44" />

### Fejlende og skippede tests

<img width="1306" height="734" alt="Failed" src="https://github.com/user-attachments/assets/01cc4591-429f-4fe5-bcbe-267278e2574f" />

### Given / When / Then kommentarer i testfilen

<img width="1270" height="296" alt="Given When Then" src="https://github.com/user-attachments/assets/89cc2afc-a4c5-41e8-ac79-03de98f7f363" />


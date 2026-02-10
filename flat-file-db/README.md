# Flat File Database

**Opgave:** Flat file database med JSON
**Kursus:** Softwaresikkerhed — Zealand Næstved

---

## Hvorfor en flat-file database?

En flat-file database (JSON-fil) kan give mening i simple scenarier:

- **Ingen databaseserver krævet** — filen kan køre hvor som helst uden installation af MySQL, PostgreSQL osv.
- **Let at inspicere** — data kan åbnes og læses direkte i en teksteditor.
- **Velegnet til prototyper og undervisning** — fokus er på logikken, ikke på databasekonfiguration.
- **Portabel** — databasen er blot en fil der kan kopieres mellem systemer.

Ulempen er, at den ikke skalerer til mange samtidige brugere, og at den ikke har transaktionssikkerhed.

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

Testene er designet med følgende teknikker:

- **Ækvivalenspartitionering** — vi tester med gyldige data (normal oprettelse) og ugyldige data (duplikat person_id).
- **Grænseværdianalyse** — vi tester med en bruger der ikke findes (returnerer `None`).
- **Given / When / Then** — alle tests er struktureret med klare forudsætninger, handlinger og forventede resultater.

---

## Tests og funktionalitet

### Test 1: `test_create_user`
- **Given:** En tom database
- **When:** En ny bruger oprettes med gyldige data
- **Then:** Brugeren gemmes og kan læses tilbage
- **Risiko hvis testen fejler:** Brugere kan ikke oprettes — hele systemet er ubrugeligt.

### Test 2: `test_create_duplicate_user_raises_error`
- **Given:** En bruger med person_id '1' eksisterer allerede
- **When:** Vi forsøger at oprette en ny bruger med samme person_id
- **Then:** En `ValueError` kastes
- **Risiko hvis testen fejler:** Duplikerede brugere kan oprettes, hvilket ødelægger dataintegritet.

### Test 3: `test_read_nonexistent_user_returns_none`
- **Given:** En tom database
- **When:** Vi forsøger at læse en bruger der ikke findes
- **Then:** `None` returneres
- **Risiko hvis testen fejler:** Systemet kan crashe ved opslag på ikke-eksisterende brugere.

### Test 4: `test_update_user`
- **Given:** En bruger eksisterer i databasen
- **When:** Vi opdaterer brugerens adresse
- **Then:** Den nye adresse er gemt korrekt
- **Risiko hvis testen fejler:** Brugerdata kan ikke opdateres, gammel data forbliver.

### Test 5: `test_disable_user`
- **Given:** En aktiv bruger eksisterer
- **When:** Vi deaktiverer brugeren
- **Then:** Brugerens `enabled` felt er `False`
- **Risiko hvis testen fejler:** Brugere kan ikke deaktiveres — sikkerhedsrisiko ved kompromitterede konti.

### Test 6: `test_enable_user`
- **Given:** En deaktiveret bruger eksisterer
- **When:** Vi aktiverer brugeren
- **Then:** Brugerens `enabled` felt er `True`
- **Risiko hvis testen fejler:** Deaktiverede brugere kan ikke genaktiveres.

### Test 7: `test_password_is_hashed__expected_fail` (FEJLER MED VILJE)
- **Given:** En bruger oprettes med et plaintext password
- **When:** Vi læser brugeren fra databasen
- **Then:** Det gemte password burde IKKE matche plaintext — men det gør det, fordi hashing ikke er implementeret
- **Risiko hvis testen fejler:** Passwords gemmes i klartekst — alvorlig sikkerhedsrisiko.
- **Hvad skal ændres:** Implementer password-hashing (f.eks. bcrypt) i `create_user()`.

### Test 8: `test_delete_user` (SKIPPED)
- **Given:** En bruger eksisterer
- **When:** Vi sletter brugeren
- **Then:** Brugeren kan ikke længere findes
- **Hvorfor skipped:** `delete_user()` er ikke implementeret endnu.
- **Hvad skal ændres:** Implementer `delete_user(person_id)` i `flat_file_db.py`.

---

## Kør tests

```bash
cd flat-file-db
python -m pytest tests/ -v
```

---

## Test execution (screenshots)

> **Indsæt følgende screenshots manuelt:**

1. **Screenshot af PyTest output med beståede tests**
   Kør `python -m pytest tests/ -v` og tag et screenshot af terminalen der viser de grønne PASSED tests.

2. **Screenshot af PyTest output med fejlende og skippede tests**
   Samme kørsel vil vise den fejlende test (`FAILED`) og den skippede test (`SKIPPED`). Tag et screenshot af dette.

3. **Screenshot af testfilen med Given / When / Then kommentarer**
   Åbn `tests/test_flat_file_db.py` i en editor og tag et screenshot der viser de strukturerede Given / When / Then kommentarer i mindst én test.

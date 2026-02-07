# Test Strategier og Test Teknikker

## Emne: Authentication and Account Management

Denne opgave dækker teststrategier og testteknikker med fokus på:
- Login
- Password validation
- Multi-Factor Authentication (MFA)

---

## Testteknikker

### 1. Ækvivalensklasser (Equivalence Partitioning)

Opdeler input i klasser hvor alle værdier i en klasse forventes at give samme resultat.

**Eksempel - Password længde:**

| Klasse | Værdi | Forventet resultat |
|--------|-------|-------------------|
| For kort | 1-7 tegn | Afvist |
| Gyldig | 8-64 tegn | Accepteret |
| For lang | 65+ tegn | Afvist |

**Security Gate:** Code/Dev

---

### 2. Grænseværditest (Boundary Value Analysis)

Tester værdierne på og omkring grænserne mellem ækvivalensklasser.

**Eksempel - Password længde grænser:**

| Værdi | Forventet resultat |
|-------|-------------------|
| 7 tegn | Afvist (under grænse) |
| 8 tegn | Accepteret (nedre grænse) |
| 64 tegn | Accepteret (øvre grænse) |
| 65 tegn | Afvist (over grænse) |

**Security Gate:** Code/Dev

---

### 3. CRUD(L) Test

Tester de grundlæggende operationer: Create, Read, Update, Delete, List.

**Eksempel - Brugerkonto:**

| Operation | Beskrivelse | Test |
|-----------|-------------|------|
| Create | Opret ny bruger | Registrering med valid email/password |
| Read | Læs brugerdata | Hent profil efter login |
| Update | Opdater bruger | Skift password |
| Delete | Slet bruger | Slet konto |
| List | List brugere | Admin kan se alle brugere |

**Security Gate:** Integration

---

### 4. Cycle Process Test

Tester en hel livscyklus fra start til slut.

**Eksempel - Login session livscyklus:**

```
1. Bruger registrerer sig
2. Bruger logger ind
3. Session oprettes
4. Bruger udfører handlinger
5. Session timeout / bruger logger ud
6. Session invalideres
```

**Security Gate:** System

---

### 5. Decision Table Test

Tester kombinationer af betingelser og forventede resultater.

**Eksempel - Login validering:**

| Brugernavn gyldig | Password gyldig | MFA gyldig | Resultat |
|-------------------|-----------------|------------|----------|
| Nej | - | - | Afvist |
| Ja | Nej | - | Afvist |
| Ja | Ja | Nej | Afvist |
| Ja | Ja | Ja | Adgang |

Se implementering i: `tests/test_login_decision_table.py`

**Security Gate:** Code/Dev, Integration

---

### 6. Test Pyramiden

```
         /\
        /  \         E2E Tests (få)
       /    \        - Hele login flow i browser
      /------\
     /        \      Integration Tests (nogle)
    /          \     - API endpoints
   /------------\
  /              \   Unit Tests (mange)
 /                \  - Password validation
/------------------\ - Input sanitering
```

| Niveau | Eksempel | Antal | Security Gate |
|--------|----------|-------|---------------|
| Unit | Password validering | Mange | Code/Dev |
| Integration | Login API test | Nogle | Integration |
| E2E | Fuldt login flow | Få | System/Release |

---

## PyTest Implementation

### Decision Table Test

Filen `tests/test_login_decision_table.py` indeholder en data-drevet test med `@pytest.mark.parametrize`.

**Status:**
- De fleste tests består
- En test er markeret som `skip` (MFA timeout scenarie)
- En test fejler med vilje (uventet system fejl)

**Sådan rettes de:**

| Test | Problem | Løsning |
|------|---------|---------|
| MFA timeout | Skipped | Fjern `pytest.param(..., marks=pytest.mark.skip)` og implementer timeout håndtering |
| System error | Fejler | Ret `expected` fra `"error"` til `"denied"` eller implementer error håndtering |

---

## Sådan køres tests

Naviger til `test-strategier/tests` mappen og kør:

```bash
python -m pytest test_login_decision_table.py
```

For detaljeret output:

```bash
python -m pytest test_login_decision_table.py -v
```

# Encryption + Hashing

**Opgave:** Kryptering og hashing af brugerdata
**Kursus:** Softwaresikkerhed — Zealand Næstved

---

## Overvejede krypteringsalgoritmer

| Algoritme | Type | Bemærkning |
|-----------|------|------------|
| **Fernet (AES-128-CBC)** | Symmetrisk kryptering | Simpel, sikker, del af `cryptography`-biblioteket. Valgt. |
| AES-256-GCM | Symmetrisk kryptering | Stærkere, men mere kompleks opsætning. |
| RSA | Asymmetrisk kryptering | Overkill til lokal datakryptering, bruges typisk til nøgleudveksling. |

### Valg: Fernet (AES-128-CBC)

Fernet blev valgt fordi:

- Det er en del af det velkendte `cryptography`-bibliotek i Python.
- Det tilbyder authenticated encryption (integritet + fortrolighed).
- Det er simpelt at bruge og passende til undervisningsformål.
- Nøglen kan genereres med én linje kode.

---

## Overvejede hashing-algoritmer

| Algoritme | Bemærkning |
|-----------|------------|
| **bcrypt** | Langsom designet, salt inkluderet, velegnet til passwords. Valgt. |
| Argon2 | Nyere, vinder af Password Hashing Competition. Kræver ekstra pakke. |
| SHA-256 | For hurtig til passwords (sårbar over for brute-force). Ikke egnet. |
| MD5 | Broken — aldrig bruge til sikkerhed. |

### Valg: bcrypt

bcrypt blev valgt fordi:

- Det er designet specifikt til password-hashing.
- Det er langsomt med vilje (modstandsdygtig over for brute-force).
- Salt genereres automatisk og inkluderes i hashen.
- Det er bredt understøttet og velafprøvet.

---

## Hvornår data krypteres

Personlige data (navn, adresse, CPR-nummer osv.) krypteres **inden de gemmes**:

1. Brugerens personlige data modtages som plaintext.
2. Data krypteres med Fernet og den hemmelige nøgle.
3. Kun den krypterede version gemmes.

Passwords krypteres **aldrig** — de **hashes** i stedet med bcrypt.

---

## Hvornår data dekrypteres

Data dekrypteres **kun når det er nødvendigt**:

1. Den krypterede tekst hentes fra lagring.
2. Dekryptering sker med den hemmelige nøgle.
3. Den dekrypterede data bruges til det nødvendige formål (f.eks. visning).
4. Den dekrypterede data **slettes fra memory** (variablen slettes med `del`) hurtigst muligt.

---

## Hvornår dekrypteret data fjernes fra memory

Dekrypteret data bør fjernes fra memory **så snart den ikke længere bruges**:

```python
decrypted = decrypt_data(encrypted_text, key)
# ... brug data ...
del decrypted  # Fjern fra memory
```

Dette reducerer risikoen for at følsomme data kan udtrækkes fra hukommelsen (f.eks. ved memory dumps eller side-channel attacks).

---

## GDPR-overvejelser

| Princip | Implementering |
|---------|---------------|
| **Dataminimering** | Gem kun nødvendige data. |
| **Fortrolighed** | Personlige data krypteres med Fernet. |
| **Integritet** | Fernet giver authenticated encryption — data kan ikke ændres uden at det opdages. |
| **Retten til sletning** | Slet den krypterede data. Alternativt kan krypteringsnøglen destrueres ("crypto-shredding"). |
| **Pseudonymisering** | Kryptering gør data ulæselig uden nøgle. |

**Crypto-shredding:** Ved at slette krypteringsnøglen bliver al data krypteret med den nøgle ubrugelig. Dette er en effektiv måde at implementere "retten til at blive glemt" under GDPR.

---

## Sikkerhedsovervejelser

- **Passwords hashes, aldrig krypteres.** Hashing er one-way — selv med adgang til databasen kan passwords ikke udtrækkes.
- **Krypteringsnøglen skal opbevares sikkert.** Hvis nøglen kompromitteres, kan al krypteret data læses.
- **Brug altid salt.** bcrypt gør dette automatisk.
- **Dekrypteret data skal fjernes fra memory.** Brug `del` på variabler med følsomme data.
- **Brug ikke MD5 eller SHA-256 til passwords.** De er for hurtige og sårbare over for brute-force.
- **Nøglen bør ikke gemmes sammen med dataen.** I praksis bruges key management services (KMS).

---

## Kør tests

```bash
cd crypto-hashing
python -m pytest tests/ -v
```

**Kræver:**
```bash
pip install bcrypt cryptography
```

---

## Test execution (screenshots)


1. **Screenshot af PyTest output med beståede crypto-tests**
   Kør `python -m pytest tests/ -v` og tag et screenshot af terminalen der viser de grønne PASSED tests.
<img width="1268" height="315" alt="cpassed" src="https://github.com/user-attachments/assets/d819185c-50a9-4c13-b233-bf02b142a8d5" />

2. **Screenshot af PyTest output med fejlende og skippede crypto-tests**
   Samme kørsel vil vise den fejlende test (`FAILED`) og den skippede test (`SKIPPED`). Tag et screenshot af dette.
<img width="1289" height="626" alt="cfailed" src="https://github.com/user-attachments/assets/b3d1d83d-d0e0-4feb-937a-e12be9c39617" />

3. **Screenshot af terminal-output fra PyTest**
   Tag et screenshot af den fulde terminal-output efter kørsel af alle tests, inklusiv summary-linjen der viser antal passed, failed og skipped.
   <img width="1277" height="822" alt="tests" src="https://github.com/user-attachments/assets/c7b7db52-50a1-43f6-a287-dc98ea32e29a" />


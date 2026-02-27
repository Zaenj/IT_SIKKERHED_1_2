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

Jeg valgte Fernet fordi:

- Det er en del af `cryptography` biblioteket i Python, som er velkendt og bredt brugt.
- Det giver både kryptering og integritetstjek, så man kan se hvis data er blevet ændret.
- Det er simpelt at bruge, nøglen kan genereres med én linje kode.
- Til en skoleopgave er det mere end rigeligt.

---

## Overvejede hashing-algoritmer

| Algoritme | Bemærkning |
|-----------|------------|
| **bcrypt** | Langsom designet, salt inkluderet, velegnet til passwords. Valgt. |
| Argon2 | Nyere, vinder af Password Hashing Competition. Kræver ekstra pakke. |
| SHA-256 | For hurtig til passwords (sårbar over for brute-force). Ikke egnet. |
| MD5 | Broken — aldrig bruge til sikkerhed. |

### Valg: bcrypt

Jeg valgte bcrypt fordi:

- Det er lavet specifikt til passwords, ikke til generel hashing.
- Det er langsomt med vilje, det gør brute-force meget sværere.
- Salt bliver genereret automatisk og gemt som en del af hashen.
- Det er velafprøvet og bruges i mange projekter.

---

## Hvornår data krypteres

Personlige data (navn, adresse, CPR osv.) krypteres **inden de gemmes**:

1. Data kommer ind som plaintext.
2. Det krypteres med Fernet og den hemmelige nøgle.
3. Kun den krypterede version gemmes i databasen.

Passwords krypteres **aldrig** — de hashes med bcrypt i stedet, fordi man aldrig skal kunne læse et password tilbage.

---

## Hvornår data dekrypteres

Data dekrypteres **kun når det faktisk er nødvendigt**:

1. Den krypterede tekst hentes fra filen.
2. Den dekrypteres med nøglen.
3. Data bruges til det den skal (f.eks. vises til brugeren).
4. Bagefter slettes den dekrypterede data fra memory med `del`.

---

## Hvornår dekrypteret data fjernes fra memory

Man bør fjerne dekrypteret data fra memory **så snart man er færdig med at bruge det**:

```python
decrypted = decrypt_data(encrypted_text, key)
# ... brug data ...
del decrypted  # Fjern fra memory
```

Pointen er at følsomme data ikke bare skal ligge i hukommelsen længere end nødvendigt. Ellers risikerer man at det kan læses via memory dumps.

---

## GDPR-overvejelser

| Princip | Implementering |
|---------|---------------|
| **Dataminimering** | Gem kun nødvendige data. |
| **Fortrolighed** | Personlige data krypteres med Fernet. |
| **Integritet** | Fernet giver authenticated encryption — data kan ikke ændres uden at det opdages. |
| **Retten til sletning** | Slet den krypterede data. Alternativt kan krypteringsnøglen destrueres ("crypto-shredding"). |
| **Pseudonymisering** | Kryptering gør data ulæselig uden nøgle. |

**Crypto-shredding:** Hvis man sletter krypteringsnøglen, kan al data der er krypteret med den aldrig læses igen. Det er en smart måde at "slette" store mængder data på — man sletter bare nøglen i stedet for alt dataen.

---

## Sikkerhedsovervejelser

- Passwords skal altid hashes, aldrig krypteres. Hashing er one-way, så selv hvis nogen får adgang til databasen, kan de ikke læse passwords.
- Krypteringsnøglen skal opbevares et sikkert sted. Hvis nøglen lækker, kan al krypteret data læses.
- Brug altid salt til password-hashing — bcrypt gør det automatisk.
- Dekrypteret data bør slettes fra memory (`del`) når man er færdig med det.
- MD5 og SHA-256 er for hurtige til passwords og kan brute-forces. Brug bcrypt eller Argon2 i stedet.
- Nøglen bør ikke gemmes i samme fil som dataen. I praksis bruger man en key management service (KMS).

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

### Beståede tests

<img width="1268" height="315" alt="Passed crypto tests" src="https://github.com/user-attachments/assets/d819185c-50a9-4c13-b233-bf02b142a8d5" />

### Fejlende og skippede tests

<img width="1289" height="626" alt="Failed crypto tests" src="https://github.com/user-attachments/assets/b3d1d83d-d0e0-4feb-937a-e12be9c39617" />

### Fuld terminal-output fra PyTest

<img width="1277" height="822" alt="Full PyTest output" src="https://github.com/user-attachments/assets/c7b7db52-50a1-43f6-a287-dc98ea32e29a" />


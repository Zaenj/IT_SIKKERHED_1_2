# PyTest Intro

## Hvad er PyTest?

PyTest er et testframework til Python, der gør det nemt at skrive og køre tests.

---

## Hvad demonstrerer denne opgave?

Denne opgave viser grundlæggende PyTest funktionalitet:

- **Passing test** - en test der består
- **Failing test** - en test der fejler (med vilje)
- **Skipped test** - en test der springes over

---

## Testfil

Alle tests findes i: `tests/test_basic.py`

---

## Hvorfor fejler eller springes nogle tests over?

### Failing test: `test_intentional_fail`

Denne test fejler fordi den påstår at `1 + 1 == 3`, hvilket er forkert.

**Sådan rettes den:**
Ret assertion til `assert 1 + 1 == 2`

### Skipped test: `test_skipped_feature`

Denne test er markeret med `@pytest.mark.skip` og køres derfor ikke.

**Sådan rettes den:**
Fjern `@pytest.mark.skip` dekoratoren og ret assertion til `assert 2 * 2 == 4`

---

## Sådan køres tests

Naviger til `pytest-intro/tests` mappen og kør:

```bash
python -m pytest test_basic.py
```

For mere detaljeret output:

```bash
python -m pytest test_basic.py -v
```

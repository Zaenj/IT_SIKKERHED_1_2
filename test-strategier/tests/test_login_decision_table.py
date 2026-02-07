"""
test_login_decision_table.py

Decision Table Test for Authentication

Denne test demonstrerer en beslutnings-tabel (decision table) for login validering.
Testen bruger @pytest.mark.parametrize til at køre multiple test cases.

Emne: Authentication and Account Management
"""

import pytest


def validate_login(username_valid: bool, password_valid: bool, mfa_valid: bool) -> str:
    """
    Simulerer login validering baseret på tre betingelser.

    Args:
        username_valid: Er brugernavnet gyldigt?
        password_valid: Er password gyldigt?
        mfa_valid: Er MFA koden gyldig?

    Returns:
        "granted" - hvis alle betingelser er opfyldt
        "denied" - hvis en eller flere betingelser fejler
    """
    if username_valid and password_valid and mfa_valid:
        return "granted"
    return "denied"


# Decision Table:
# | username_valid | password_valid | mfa_valid | expected |
# |----------------|----------------|-----------|----------|
# | False          | False          | False     | denied   |
# | False          | True           | True      | denied   |
# | True           | False          | True      | denied   |
# | True           | True           | False     | denied   |
# | True           | True           | True      | granted  |

@pytest.mark.parametrize(
    "username_valid, password_valid, mfa_valid, expected",
    [
        # Test case 1: Alt er ugyldigt
        (False, False, False, "denied"),

        # Test case 2: Kun brugernavn er ugyldigt
        (False, True, True, "denied"),

        # Test case 3: Kun password er ugyldigt
        (True, False, True, "denied"),

        # Test case 4: Kun MFA er ugyldig
        (True, True, False, "denied"),

        # Test case 5: Alt er gyldigt - adgang gives
        (True, True, True, "granted"),

        # Test case 6: SKIPPED - MFA timeout scenarie
        # Denne test er sprunget over fordi MFA timeout ikke er implementeret endnu
        # FOR AT FÅ TESTEN TIL AT BESTÅ:
        # 1. Fjern marks=pytest.mark.skip
        # 2. Implementer timeout håndtering i validate_login funktionen
        pytest.param(
            True, True, False, "timeout",
            marks=pytest.mark.skip(reason="MFA timeout ikke implementeret endnu")
        ),

        # Test case 7: FAILS - System error scenarie
        # Denne test FEJLER med vilje for at demonstrere en uventet fejl
        # FOR AT FÅ TESTEN TIL AT BESTÅ:
        # Ret expected fra "error" til "denied" (eller implementer error håndtering)
        (False, False, True, "error"),  # Forventet: error, Faktisk: denied
    ],
)
def test_login_decision_table(username_valid, password_valid, mfa_valid, expected):
    """
    Data-drevet test der verificerer login beslutningslogik.

    Tester alle kombinationer af:
    - Gyldigt/ugyldigt brugernavn
    - Gyldigt/ugyldigt password
    - Gyldig/ugyldig MFA kode
    """
    result = validate_login(username_valid, password_valid, mfa_valid)
    assert result == expected, f"Forventede '{expected}', fik '{result}'"

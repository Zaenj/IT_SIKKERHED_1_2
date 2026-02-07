"""
test_basic.py

Demonstrerer grundlæggende PyTest funktionalitet:
- Passing test
- Failing test (intentional)
- Skipped test
"""

import pytest


def test_passing():
    """
    Denne test består.
    Den verificerer at 1 + 1 er lig med 2.
    """
    assert 1 + 1 == 2


def test_intentional_fail():
    """
    Denne test FEJLER med vilje.

    Den påstår at 1 + 1 == 3, hvilket er forkert.

    FOR AT FÅ TESTEN TIL AT BESTÅ:
    Ret linjen til: assert 1 + 1 == 2
    """
    assert 1 + 1 == 3  # Dette er forkert - testen fejler


@pytest.mark.skip(reason="Denne test er sprunget over med vilje")
def test_skipped_feature():
    """
    Denne test SPRINGES OVER med vilje.

    FOR AT FÅ TESTEN TIL AT BESTÅ:
    1. Fjern @pytest.mark.skip dekoratoren ovenfor
    2. Ret linjen til: assert 2 * 2 == 4
    """
    assert 2 * 2 == 5  # Dette er også forkert

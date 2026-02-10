"""
Tests for crypto_utils.py.

Tests password hashing (bcrypt) and data encryption (Fernet/AES).
Uses Given / When / Then comments to describe each test scenario.
"""

import os
import sys
import pytest

# Add the src folder to the path so we can import crypto_utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import crypto_utils


# ──────────────────────────────────────────────
# TEST: Hash password
# ──────────────────────────────────────────────
def test_hash_password_differs_from_plaintext():
    """
    GIVEN: A plaintext password
    WHEN:  The password is hashed with bcrypt
    THEN:  The hash is different from the plaintext
    """
    # Given
    plaintext = "SuperHemmeligt123"

    # When
    hashed = crypto_utils.hash_password(plaintext)

    # Then
    assert hashed != plaintext
    assert len(hashed) > 0


# ──────────────────────────────────────────────
# TEST: Verify correct password
# ──────────────────────────────────────────────
def test_verify_correct_password():
    """
    GIVEN: A password has been hashed with bcrypt
    WHEN:  We verify the original plaintext against the hash
    THEN:  The verification returns True
    """
    # Given
    plaintext = "SuperHemmeligt123"
    hashed = crypto_utils.hash_password(plaintext)

    # When
    result = crypto_utils.verify_password(plaintext, hashed)

    # Then
    assert result is True


# ──────────────────────────────────────────────
# TEST: Verify wrong password
# ──────────────────────────────────────────────
def test_verify_wrong_password():
    """
    GIVEN: A password has been hashed with bcrypt
    WHEN:  We verify a WRONG password against the hash
    THEN:  The verification returns False
    """
    # Given
    hashed = crypto_utils.hash_password("SuperHemmeligt123")

    # When
    result = crypto_utils.verify_password("ForkertPassword", hashed)

    # Then
    assert result is False


# ──────────────────────────────────────────────
# TEST: Encrypt and decrypt data
# ──────────────────────────────────────────────
def test_encrypt_and_decrypt_data():
    """
    GIVEN: A plaintext string and an encryption key
    WHEN:  The string is encrypted and then decrypted
    THEN:  The decrypted result matches the original plaintext
    """
    # Given
    key = crypto_utils.generate_key()
    original = "Anders Jensen, Parkvej 12, 4700 Næstved"

    # When
    encrypted = crypto_utils.encrypt_data(original, key)
    decrypted = crypto_utils.decrypt_data(encrypted, key)

    # Then
    assert encrypted != original  # Encrypted text must differ from plaintext
    assert decrypted == original  # Decrypted text must match original


# ──────────────────────────────────────────────
# TEST: Encrypted data is not readable
# ──────────────────────────────────────────────
def test_encrypted_data_is_not_readable():
    """
    GIVEN: Personal data is encrypted with Fernet
    WHEN:  We inspect the encrypted output
    THEN:  The original data cannot be read from the encrypted string
    """
    # Given
    key = crypto_utils.generate_key()
    personal_data = "CPR: 010199-1234"

    # When
    encrypted = crypto_utils.encrypt_data(personal_data, key)

    # Then
    assert "010199" not in encrypted
    assert "1234" not in encrypted


# ──────────────────────────────────────────────
# TEST: Decryption with wrong key fails
# ──────────────────────────────────────────────
def test_decrypt_with_wrong_key_fails():
    """
    GIVEN: Data encrypted with one key
    WHEN:  We try to decrypt with a different key
    THEN:  An exception is raised
    """
    # Given
    key1 = crypto_utils.generate_key()
    key2 = crypto_utils.generate_key()
    encrypted = crypto_utils.encrypt_data("Hemmelig data", key1)

    # When / Then
    with pytest.raises(Exception):
        crypto_utils.decrypt_data(encrypted, key2)


# ──────────────────────────────────────────────
# TEST: Intentionally FAILING test
# ──────────────────────────────────────────────
def test_hash_is_reversible__expected_fail():
    """
    GIVEN: A password has been hashed with bcrypt
    WHEN:  We try to "decrypt" (reverse) the hash back to plaintext
    THEN:  We expect to get the original password back

    NOTE: This test INTENTIONALLY FAILS because bcrypt is a ONE-WAY hash.
    There is no function to reverse a bcrypt hash — that is the whole point.

    TO MAKE IT PASS: This test should NOT pass. It demonstrates that
    hashing is irreversible, which is the correct security behavior.
    """
    # Given
    plaintext = "SuperHemmeligt123"
    hashed = crypto_utils.hash_password(plaintext)

    # When / Then — This WILL FAIL because hashing is one-way
    assert hashed == plaintext, (
        "bcrypt hash cannot be reversed to plaintext. This is expected and correct."
    )


# ──────────────────────────────────────────────
# TEST: Intentionally SKIPPED test
# ──────────────────────────────────────────────
@pytest.mark.skip(reason="Argon2 is not installed. Only bcrypt is used in this assignment.")
def test_argon2_hashing():
    """
    GIVEN: A plaintext password
    WHEN:  The password is hashed with Argon2
    THEN:  The hash differs from the plaintext

    NOTE: This test is SKIPPED because Argon2 requires the 'argon2-cffi' package
    which is not installed. This assignment uses bcrypt instead.

    TO MAKE IT PASS: Install argon2-cffi (pip install argon2-cffi)
    and implement an argon2_hash_password() function in crypto_utils.py.
    """
    from argon2 import PasswordHasher

    ph = PasswordHasher()
    hashed = ph.hash("SuperHemmeligt123")
    assert hashed != "SuperHemmeligt123"

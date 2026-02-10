"""
Tests for flat file database (flat_file_db.py).

Uses Given / When / Then comments to describe each test scenario.
"""

import json
import os
import sys
import pytest

# Add the src folder to the path so we can import flat_file_db
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import flat_file_db

# Path to the test database
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "users.json")


@pytest.fixture(autouse=True)
def clean_db():
    """Reset the database before and after each test."""
    with open(TEST_DB_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    yield
    with open(TEST_DB_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)


# ──────────────────────────────────────────────
# TEST: Create user
# ──────────────────────────────────────────────
def test_create_user():
    """
    GIVEN: An empty database
    WHEN:  A new user is created with valid data
    THEN:  The user is stored in the database and can be read back
    """
    # Given
    # Database is empty (handled by fixture)

    # When
    user = flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
        enabled=True,
    )

    # Then
    assert user["person_id"] == "1"
    assert user["first_name"] == "Anders"
    assert user["last_name"] == "Jensen"
    stored = flat_file_db.read_user("1")
    assert stored is not None
    assert stored["first_name"] == "Anders"


# ──────────────────────────────────────────────
# TEST: Create duplicate user raises error
# ──────────────────────────────────────────────
def test_create_duplicate_user_raises_error():
    """
    GIVEN: A user with person_id '1' already exists in the database
    WHEN:  We try to create another user with the same person_id
    THEN:  A ValueError is raised
    """
    # Given
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
    )

    # When / Then
    with pytest.raises(ValueError):
        flat_file_db.create_user(
            person_id="1",
            first_name="Bo",
            last_name="Hansen",
            address="Skovvej",
            street_number="5",
            password="password456",
        )


# ──────────────────────────────────────────────
# TEST: Read user that does not exist
# ──────────────────────────────────────────────
def test_read_nonexistent_user_returns_none():
    """
    GIVEN: An empty database
    WHEN:  We try to read a user with a person_id that does not exist
    THEN:  None is returned
    """
    # Given
    # Database is empty

    # When
    result = flat_file_db.read_user("999")

    # Then
    assert result is None


# ──────────────────────────────────────────────
# TEST: Update user
# ──────────────────────────────────────────────
def test_update_user():
    """
    GIVEN: A user exists in the database
    WHEN:  We update the user's address
    THEN:  The updated address is stored correctly
    """
    # Given
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
    )

    # When
    updated = flat_file_db.update_user("1", address="Skovvej", street_number="99")

    # Then
    assert updated["address"] == "Skovvej"
    assert updated["street_number"] == "99"


# ──────────────────────────────────────────────
# TEST: Disable user
# ──────────────────────────────────────────────
def test_disable_user():
    """
    GIVEN: An enabled user exists in the database
    WHEN:  We disable the user
    THEN:  The user's enabled field is False
    """
    # Given
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
        enabled=True,
    )

    # When
    flat_file_db.disable_user("1")

    # Then
    user = flat_file_db.read_user("1")
    assert user["enabled"] is False


# ──────────────────────────────────────────────
# TEST: Enable user
# ──────────────────────────────────────────────
def test_enable_user():
    """
    GIVEN: A disabled user exists in the database
    WHEN:  We enable the user
    THEN:  The user's enabled field is True
    """
    # Given
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
        enabled=False,
    )

    # When
    flat_file_db.enable_user("1")

    # Then
    user = flat_file_db.read_user("1")
    assert user["enabled"] is True


# ──────────────────────────────────────────────
# TEST: Intentionally FAILING test
# ──────────────────────────────────────────────
def test_password_is_hashed__expected_fail():
    """
    GIVEN: A user is created with a plaintext password
    WHEN:  We read the user from the database
    THEN:  The stored password should NOT equal the plaintext password
           (i.e., it should be hashed)

    NOTE: This test INTENTIONALLY FAILS because the current implementation
    stores passwords in plaintext. This is a known security issue.

    TO MAKE IT PASS: Integrate password hashing (e.g. bcrypt) in create_user()
    so that the stored password differs from the plaintext input.
    """
    # Given
    plaintext_password = "hemmeligt123"
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password=plaintext_password,
    )

    # When
    user = flat_file_db.read_user("1")

    # Then — this WILL FAIL because the password is stored as plaintext
    assert user["password"] != plaintext_password, (
        "Password is stored in plaintext! It should be hashed."
    )


# ──────────────────────────────────────────────
# TEST: Intentionally SKIPPED test
# ──────────────────────────────────────────────
@pytest.mark.skip(reason="Delete functionality is not yet implemented.")
def test_delete_user():
    """
    GIVEN: A user exists in the database
    WHEN:  We delete the user
    THEN:  The user can no longer be found

    NOTE: This test is SKIPPED because delete_user() does not exist yet.

    TO MAKE IT PASS: Implement a delete_user(person_id) function in flat_file_db.py
    that removes the user from the JSON file.
    """
    # Given
    flat_file_db.create_user(
        person_id="1",
        first_name="Anders",
        last_name="Jensen",
        address="Parkvej",
        street_number="12",
        password="hemmeligt123",
    )

    # When
    flat_file_db.delete_user("1")

    # Then
    assert flat_file_db.read_user("1") is None

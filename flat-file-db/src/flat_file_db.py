"""
Flat file database using JSON for user storage.
Supports: create, read, update, enable/disable users.
"""

import json
import os

# Path to the JSON database file
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "users.json")


def _load_db():
    """Load users from the JSON file. Returns a list of user dicts."""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = f.read().strip()
        if not data:
            return []
        return json.loads(data)


def _save_db(users):
    """Save the list of users to the JSON file."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def create_user(person_id, first_name, last_name, address, street_number, password, enabled=True):
    """
    Create a new user and add to the database.
    Raises ValueError if person_id already exists.
    """
    users = _load_db()

    for user in users:
        if user["person_id"] == person_id:
            raise ValueError(f"User with person_id '{person_id}' already exists.")

    new_user = {
        "person_id": person_id,
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "street_number": street_number,
        "password": password,
        "enabled": enabled,
    }

    users.append(new_user)
    _save_db(users)
    return new_user


def read_user(person_id):
    """
    Read a user by person_id.
    Returns the user dict or None if not found.
    """
    users = _load_db()
    for user in users:
        if user["person_id"] == person_id:
            return user
    return None


def update_user(person_id, **fields):
    """
    Update fields on an existing user.
    Only the provided keyword arguments are updated.
    Raises ValueError if the user does not exist.
    """
    users = _load_db()

    for user in users:
        if user["person_id"] == person_id:
            for key, value in fields.items():
                if key not in user:
                    raise ValueError(f"Unknown field: '{key}'")
                user[key] = value
            _save_db(users)
            return user

    raise ValueError(f"User with person_id '{person_id}' not found.")


def enable_user(person_id):
    """Enable a user account (set enabled=True)."""
    return update_user(person_id, enabled=True)


def disable_user(person_id):
    """Disable a user account (set enabled=False)."""
    return update_user(person_id, enabled=False)

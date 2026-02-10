"""
Crypto utilities for password hashing and personal data encryption.

- Passwords are HASHED (one-way) using bcrypt.
- Personal data is ENCRYPTED (two-way) using Fernet (AES-128-CBC).
"""

import bcrypt
from cryptography.fernet import Fernet


# ──────────────────────────────────────────────
# ENCRYPTION (for personal data)
# ──────────────────────────────────────────────

def generate_key():
    """Generate a new Fernet encryption key."""
    return Fernet.generate_key()


def encrypt_data(plaintext, key):
    """
    Encrypt a plaintext string using Fernet (AES-128-CBC).
    Returns the encrypted bytes as a string.
    """
    f = Fernet(key)
    encrypted = f.encrypt(plaintext.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt_data(encrypted_text, key):
    """
    Decrypt an encrypted string using Fernet.
    Returns the original plaintext string.

    After use, the caller should delete the decrypted value
    from memory as soon as possible (del variable).
    """
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_text.encode("utf-8"))
    return decrypted.decode("utf-8")


# ──────────────────────────────────────────────
# HASHING (for passwords)
# ──────────────────────────────────────────────

def hash_password(plaintext_password):
    """
    Hash a plaintext password using bcrypt.
    Returns the hashed password as a string.

    bcrypt automatically generates a salt and includes it in the hash.
    """
    password_bytes = plaintext_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plaintext_password, hashed_password):
    """
    Verify a plaintext password against a bcrypt hash.
    Returns True if the password matches, False otherwise.
    """
    password_bytes = plaintext_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

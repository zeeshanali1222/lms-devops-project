"""
auth_system.py - Group F: Authentication Module

Purpose: Authenticate users (librarians/members).
Responsibilities: Basic login system.

Note: This is a simple in-memory authentication system intended for
demonstration/educational purposes. Passwords are stored in plain text in
user_db, which is NOT suitable for production use.
"""


def authenticate(username, password, user_db):
    """Check whether the given username/password pair is valid.

    Args:
        username (str): The username attempting to log in.
        password (str): The password supplied.
        user_db (dict): Mapping of username -> password.

    Returns:
        bool: True if the credentials match, False otherwise.
    """
    return user_db.get(username) == password


def register_user(username, password, user_db):
    """Register a new user in the user database.

    Args:
        username (str): The desired username.
        password (str): The desired password.
        user_db (dict): Mapping of username -> password to update.

    Returns:
        bool: True if registration succeeded, False if the username
            already exists.
    """
    if username in user_db:
        return False
    user_db[username] = password
    return True

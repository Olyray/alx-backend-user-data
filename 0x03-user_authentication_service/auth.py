#!/usr/bin/env python3
"""The authentication module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

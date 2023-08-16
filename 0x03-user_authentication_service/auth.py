#!/usr/bin/env python3
"""The authentication module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """Returns a string representation of uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            added_user = self._db.add_user(email, hashed_password)
            return added_user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a login is valid"""
        try:
            found_user = self._db.find_user_by(email=email)
            if found_user:
                return bcrypt.checkpw(
                    password.encode('utf-8'), found_user.hashed_password)
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session and returns the user's UUID"""
        try:
            found_user = self._db.find_user_by(email=email)
            user_uuid = _generate_uuid()
            self._db.update_user(found_user.id, session_id=user_uuid)
            return user_uuid
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Gets a user from the session_id"""
        try:
            gotten_user = self._db.find_user_by(session_id=session_id)
            return gotten_user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Ends a user's session"""
        return self._db.update_user(user_id, session_id=None)

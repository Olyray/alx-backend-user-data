#!/usr/bin/env python3
"""Creates the sessionauth child class"""

from .auth import Auth
import uuid
from models.user import User
from flask import request
from typing import TypeVar


class SessionAuth(Auth):
    """
    The class to implement SessionAuth

    >>> from api.v1.auth.session_auth import SessionAuth
    >>> sa = SessionAuth()
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        A function to create a session

        >>> user_id_1 = "abcde"
        >>> sa.create_session(user_id_1)
        '234abf97-b9da-4191-890e-a2108130011b'
        """
        if (
           user_id is None
           or not isinstance(user_id, str)):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A function that returns the user id from the
        user_id_by_session_id dict

        >>> user_id_1 = "abcde"
        >>> sesion_id = sa.create_session(user_id_1)
        >>> session_id = sa.create_session(user_id_1)
        >>> sa.user_id_for_session_id(session_id)
        'abcde'
        """
        if (
           session_id is None
           or not isinstance(session_id, str)
           ):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a user from a request

        >>> current_user(request)
        >>> <models.user.User object at 0x7fb8c29dbb80>
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

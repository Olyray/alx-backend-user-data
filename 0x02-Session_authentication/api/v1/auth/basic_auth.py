#!/usr/bin/env python3
"""Creates the basic auth class"""

from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Implementation of the class BasicAuth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """A function to extract the Base64 part of the Authorization header"""
        if (
           authorization_header is None
           or not isinstance(authorization_header, str)
           ):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header.split()[1]
        else:
            return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """A function to decode a Base64 string"""
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
           ):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        A function to extract the user credentials from a Base64 decoded value
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ':' not in decoded_base64_authorization_header
           ):
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user using username and password
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> User:
        """
        Retrieve the User instance for a request
        """
        print("current_user was used")
        if request is None:
            return None
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_part = self.extract_base64_authorization_header(
            authorization_header)
        if base64_part is None:
            return None
        decoded_credentials = self.decode_base64_authorization_header(
            base64_part)
        if decoded_credentials is None:
            return None
        user_name, user_pwd = self.extract_user_credentials(
            decoded_credentials)
        if user_name is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_name, user_pwd)

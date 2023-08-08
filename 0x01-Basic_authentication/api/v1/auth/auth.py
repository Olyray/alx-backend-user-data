#!/usr/bin/env python3
"""Creates a class to manage the API authentication"""
from flask import request
from typing import TypeVar, List


class Auth:
    """The class for API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        if (path is None
            or excluded_paths is None 
            or len(excluded_paths) == 0):
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

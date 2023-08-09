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
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                # Remove the asterisk at the end of the excluded path
                base_excluded_path = excluded_path[:-1]
                if path.startswith(base_excluded_path):
                    return False
            elif path == excluded_path or path + '/' == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        if request is None or 'Authorization' not in request.headers:
            return None
        if 'Authorization' in request.headers:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

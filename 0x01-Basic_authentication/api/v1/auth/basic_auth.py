#!/usr/bin/env python3
"""Creates the basic auth class"""

from .auth import Auth


class BasicAuth(Auth):
    """Implementation of the class BasicAuth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        if (
           authorization_header is None
           or not isinstance(authorization_header, str)
           ):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header.split()[1]
        else:
            return None

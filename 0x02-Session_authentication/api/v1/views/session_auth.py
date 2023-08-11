#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple
from flask import jsonify, request, abort

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handles the login route for session authentication.
    Returns:
      - JSON representation of a User object or error message.
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    # Check for missing email or password
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Route to logout and delete session"""
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})

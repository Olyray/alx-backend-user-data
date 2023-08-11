#!/usr/bin/env python3
"""
A module to handle all the routes for Session Authentication
"""
from flask import jsonify, abort, Flask, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """A post route"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user_instance = User.search({'email': email})
    if len(user_instance) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if user_instance[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user_instance[0].id)
    instance_rep = jsonify(user_instance[0].to_json())
    instance_rep.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return instance_rep

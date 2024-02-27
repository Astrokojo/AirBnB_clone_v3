#!/usr/bin/python3
"""A Flask route that returns json status response of users module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, user

User = user.User


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new user"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201



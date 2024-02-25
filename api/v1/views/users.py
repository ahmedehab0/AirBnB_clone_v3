#!/usr/bin/python3
"""users rest"""


from models import storage
from models.user import User
from api.v1.views import app_views
import json
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """GET method"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user():
    """GET method"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete method"""
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """POST method"""
    try:
        data = request.get_json()
    except json.decoder.JSONDecodeError:
        abort(400, "Not a JSON")

    email = data.get("email")
    password = data.get("password")
    if not email:
        abort(404, "Missing email")
    elif not password:
        abort(404, "Missing Password")

    user = User(email=email, password=password)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """PUT method"""
    user = storage.get(User, user_id)
    payload = request.get_json()
    if not user:
        abort(404)
    if not payload:
        abort(400, description="Not a JSON")

    for key, value in user.to_dict().items():
        if key not in ["id", "email", "created_at", "updated_at", "__class__"]:
            if key in payload:
                setattr(user, key, payload[key])
    user.save()

    return jsonify(user.to_dict())

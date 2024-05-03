#!/usr/bin/python3
"""This module contains the endpoints for Amenity resources."""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def show_users():
    """Show all the users """
    users = storage.all("User").values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", strict_slashes=False)
def show_user(user_id):
    """Show a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user"""
    if not request.is_json:
        abort(400)
    request_body = request.get_json()
    if "email" not in request_body:
        return jsonify(error="Missing email"), 400
    if "password" not in request_body:
        return jsonify(error="Missing password"), 400
    new_user = User(**request_body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400)
    request_body = request.get_json()
    for key, value in request_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

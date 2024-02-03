#!/usr/bin/python3
"""
view for User object that handles all defaults RESTFUL API actions
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """
    returns the user under the give id
    Args:
        user_id (str): state's id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users():
    """
    returns the city object under the given id
    Args:
        city_id (str): id of the city to return_
    """
    users_list = []
    users = storage.all(User)
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def get_rid_of_user(user_id):
    """
    delette a user
    Args:
        user_id (str): city id to delete
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """
    create a new instance of |User
    Returns:
        obj: new user
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data.keys():
        abort(400, "Missing email")
    if "password" not in data.keys():
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """
    update the user by id
    Args:
        user_id (str): user's id to update
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

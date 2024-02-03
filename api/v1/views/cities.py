#!/usr/bin/python3
"""
view for City object that handles all defaults RESTFUL API actions
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, City, State
import requests
import json


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["GET"])
def cities_by_id(state_id):
    """
    returns list of cities under the give state's id
    Args:
        state_id (str): state's id
    """
    tmp = []
    cities = storage.all(City)

    if storage.get(State, state_id) is None:
        abort(404)
    for city in cities.values():
        if state_id == city.state_id:
            tmp.append(city.to_dict())
    return jsonify(tmp)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def city_by_id(city_id):
    """
    returns the city object under the given id
    Args:
        city_id (str): id of the city to return_
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def get_rid_of_city(city_id):
    """
    delette a city
    Args:
        city_id (str): city id to delete
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def update_state_id(state_id):
    """
    create a new instance of City
    Args:
        state_id (str): state's id
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if "name" not in data.keys():
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def create_city(city_id):
    """
    update the city by states
    Args:
        state_id (str): state's id
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

#!/usr/bin/python3
"""
view for City object that handles all defaults RESTFUL API actions
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, City, Place
import requests
import json


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
def places_by_id(city_id):
    """
    returns list of places under the give city's id
    Args:
        city_id (str): city's id
    """
    tmp = []
    places = storage.all(Place)

    if storage.get(City, city_id) is None:
        abort(404)
    for place in places.values():
        if city_id == place.city_id:
            tmp.append(place.to_dict())
    return jsonify(tmp)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def place_by_id(place_id):
    """
    returns the place object under the given id
    Args:
        place_id (str): id of the city to return_
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def get_rid_of_place(place_id):
    """
    delette a place
    Args:
        place_id (str): place id to delete
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def update_place_by_id(city_id):
    """
    update  an instance of City
    Args:
        city_id (str): city's id
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a json")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if "name" not in data.keys():
        abort(400, "Missing name")
    if "user_id" not in data.keys():
        abort(400, "Missing user_id")
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """
    update the place by given id
    Args:
        place_id (str): place's id to update
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a json")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id" ,  "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

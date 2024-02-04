#!/usr/bin/python3
"""
view for City object that handles all defaults RESTFUL API actions
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, Place, Amenity
import requests
import json


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False, methods=["GET"])
def cities_by_id(place_id):
    """
    returns list of cities under the give state's id
    Args:
        state_id (str): state's id
    """
    tmp = []
    amenities = storage.all(Amenity)

    if storage.get(Place, place_id) is None:
        abort(404)
    for amenity in amenities.values():
        if place_id == amenity.place_id:
            tmp.append(amenity.to_dict())
    return jsonify(tmp)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def get_rid_of_city(place_id, amenity_id):
    """
    delette a city
    Args:
        city_id (str): city id to delete
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if amenity.id not in place.amenity_ids:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def update_state_id(place_id, amenity_id):
    """
    create a new instance of City
    Args:
        state_id (str): state's id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if amenity.id in place.amenity_ids:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)

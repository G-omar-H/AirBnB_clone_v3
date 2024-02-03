#!/usr/bin/python3
"""
creating route for amenities class with its requests done
"""
from flask import Flask, Blueprint, jsonify, request, make_response, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


# GET ALL
@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def all_amns():
    """retrun all the amenities object"""
    amen_list = []
    amenities = storage.all(Amenity)
    for amenty in amenities.values():
        amen_list.append(amenty.to_dict())
    return jsonify(amen_list)


# GET amenity_id
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["GET"])
def get_amin_id(amenity_id):
    """return the amenity object under the given id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


# DELETE amenity_id
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amn_id(amenity_id):
    """delete a specific amenity by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# POST /amenities
@app_views.route("/amenities",
                 strict_slashes=False, methods=["POST"])
def create_amen():
    """Creating new amenity object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    new_amnty = Amenity(**request.get_json())
    new_amnty.save()
    return jsonify(new_amnty.to_dict()), 201


# PUT /amenities/<amenity_id>
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["PUT"])
def update_amen(amenity_id):
    """update a specific amenity object by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

#!/usr/bin/python3
"""
index_
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/status", methods=['GET'])
def status_check():
    """
    return the status of the api
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """
    return raport about the objects counter
    """
    objs = {}
    for key, value in classes.items():
        objs[key] = storage.count(value)
    return jsonify(objs)

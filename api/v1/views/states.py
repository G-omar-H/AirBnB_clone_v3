#!/usr/bin/python3
"""
listing all the states
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request, make_response, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """
    get all the states
    """
    states_list = []
    states = storage.all(State)
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """
    get a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """
    create a state
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """
    update a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """
    delete a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

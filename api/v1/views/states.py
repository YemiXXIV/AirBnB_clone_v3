#!/usr/bin/python3
"""This module handles all default RESTFul APIs for State object"""

from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from models import storage
from models.state import State
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states_list():
    """Returns a list of all State objects in a json representation"""

    states = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Return a state by its id"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state using its id"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states/", methods=["POST"])
def create_state():
    """Creates a new state"""

    try:
        state = request.get_json()
    except BadRequest as e:
        abort(400, description="Not a JSON")

    if 'name' not in state:
        abort(400, description="Missing name")

    new_state = State(**state)

    storage.new(new_state)
    storage.save()

    return (jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest as e:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    storage.save()

    return (jsonify(state.to_dict()), 200)


@app_views.errorhandler(400)
def not_json(exc):
    """Handles the error (400) and returns the response in a json format"""

    return make_response(jsonify({"error": exc.description}), 400)

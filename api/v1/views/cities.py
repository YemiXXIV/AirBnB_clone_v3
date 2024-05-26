#!/usr/bin/python3
"""This module handles all default RESTFul APIs for City object"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_cities(state_id):
    """Returns a list of cities of a specific state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities_list = [city.to_dict() for city in state.cities]

    return jsonify(cities_list)

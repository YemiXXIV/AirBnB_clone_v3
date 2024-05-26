#!/usr/bin/python3
"""This module handles all default RESTFul APIs for City object"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
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


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Return a city by its id"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())

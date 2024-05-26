#!/usr/bin/python3
"""This module handles all default RESTFul APIs for Place object"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def city_places(city_id):
    """Returns a list of places of a specific City"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places_list = [place.to_dict() for place in city.places]

    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Return a place by its id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place using its id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new place that is a part of a specific city"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        place_data = request.get_json()
    except BadRequest as e:
        abort(400, description="Not a JSON")

    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, place_data['user_id'])

    if not user:
        abort(404)

    if 'name' not in place_data:
        abort(400, description="Missing name")

    new_place = Place(**place_data)
    new_place.city_id = city_id

    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        new_data = request.get_json()
    except BadRequest as e:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200

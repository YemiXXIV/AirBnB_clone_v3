#!/usr/bin/python3
"""
This module handles default RESTFul APIs for
the link between Place and Amenity objects
"""

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_amenities(place_id):
    """
    Returns list of amenities for a specific place
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities_list), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes amenity of a specific place object using id
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
        place.save()
    else:
        place.amenity_id.remove(amenity_id)

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """
    Adds amenity to a specific place object using id
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
        place.save()
    else:
        place.amenity_id.append(amenity_id)

    return jsonify(amenity.to_dict()), 201

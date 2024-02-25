#!/usr/bin/python3
"""place rest"""


from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
import json 


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_place_by_city(city_id):
    """GET method"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in storage.all(Place).values() if place.city_id == city_id]
    return jsonify(places)

@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """GET method"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """DELETE methtod"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return (jsonify({})),200
    abort(404)

@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """POST method"""
    if not storage.get(City, city_id):
        abort(404)

    try:
        data = request.get_json()
    except json.decoder.JOSNDecodeError:
        abort(400, "Not a JSON")

    user_id = data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    name = data['name']
    if not name:
        abort(400, "Missing name")

    place = Place(city_id=city_id, **data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place.

    Args:
        place_id (str): ID of the place to update.

    Returns:
        dict: Updated place in JSON.

    Raises:
        404: If the specified place_id does not exist.
        400: If the request body is not a valid JSON.
    """
    place = storage.get(Place, place_id)
    payload = request.get_json()
    if not place:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    for key, value in place.to_dict().items():
        if key not in [
            "id",
            "user_id",
            "city_id",
            "created_at",
            "updated_at",
            "__class__",
        ]:
            setattr(place, key, payload[key] if key in payload else value)
    place.save()

    return jsonify(place.to_dict())

#!/usr/bin/python3
"""amenitest rest"""


from api.v1.views import app_views
from flask import jsonify, abort, request
import json
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_ameniteis():
    """GET method"""
    amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(amenities)

@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """Get method"""
    amenity =storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete(amenity_id):
    """DELETE method"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(400)

@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create():
    """POST method"""
    try:
        data = request.get_json()
    except json.decoder.JSONDecodeError:
        abort(400, "Not a JSON")

    name = data.get("name")
    if not name:
        abort(400, "Missing name")

    amenity = Amenity(name=name)
    amenity.save()
    return (jsonify(amenity.to_dict())),201

@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update(amenity_id):
    """PUT method"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        try:
            data = request.get_json()
        except json.decoder.JSONDecodeError:
            abort(400, "Not a JSON")
        amenity.name = data.get("name")
        storage.save()
        return jsonify(amenity.to_dict()),200
    else:
        abort(404)

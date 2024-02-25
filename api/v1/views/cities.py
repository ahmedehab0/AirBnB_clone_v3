#!/usr/bin/python3
"""cities rest api"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views 
import json
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """GET method"""
    if storage.get(State, state_id):
        cities = [city.to_dict() for city in storage.all(City).values() if state_id == city.state_id]
        return jsonify(cities)
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """GET method"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """DELETE method"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """POST method"""
    if storage.get(State, state_id):
        try:
            data = request.get_json()
        except json.decoder.JSONDecodeError:
            abort(400, "Not JSON")
        if not data.get("name"):
            abort(400, "Missing name")
        city = City(name=data.get("name"), state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """PUT method"""
    city = storage.get(City, city_id)
    if city:
        try:
            data = request.get_json()
        except json.decoder.JSONDecodeError:
            abort(400, "Not JSON")
        city.name = data.get("name")
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(404)

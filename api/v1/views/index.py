#!/usr/bin/python3
"""instance of my application"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


classes = {"amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User}

@app_views.route('/status', methods=['GET'])
def status():
    """returns JSON status"""
    return jsonify({"status" : "OK"})


@app_views.route('stats', methods=['GET'])
def stats():
    """return stats"""
    json = {}
    for key, value in classes.items():
        json[key] = storage.count(value)

    return jsonify(json)
        


#!/usr/bin/python3
"""blue print to my Flask instance app"""


from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def clear(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host, port, threaded = True, debug = True)

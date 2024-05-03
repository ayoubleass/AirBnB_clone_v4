#!/usr/bin/python3
"""
This script containe the blueprint routes
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns a json response"""
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def count_objects():
    """Retrieves the number of each objects by type"""
    return jsonify(
            amenities=storage.count("Amenity"),
            cities=storage.count("City"),
            places=storage.count("Place"),
            reviews=storage.count("Review"),
            states=storage.count("State"),
            users=storage.count("User"),
    )

#!/usr/bin/python3
"""This Module has all the City end points """


from api.v1.views import app_views
from flask import jsonify
from models import storage
import json
from flask import request
from models.city import City
from flask import abort


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def show_cities(state_id):
    """Return all cities in state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in storage.all("City").values()
              if city.state_id == state_id]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def show_city(city_id):
    """Return a specifique City object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    "/cities/<city_id>",
    methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a specifique City object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a city """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400)
    request_body = request.get_json()
    if "name" not in request_body:
        return jsonify(error="Missing name"), 400
    new_city = City(name=request_body.get("name"), state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400)
    request_body = request.get_json()
    for key, value in request_body.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

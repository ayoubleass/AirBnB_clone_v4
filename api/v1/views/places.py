#!/usr/bin/python3
"""This module contains all the Place end points """

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places_by_city(city_id):
    """Show places in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """show a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    request_body = request.get_json()
    if "user_id" not in request_body:
        return jsonify(error="Missing user_id"), 400
    if "name" not in request_body:
        return jsonify("Missing name"), 400
    user_id = request_body["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    request_body["city_id"] = city_id
    new_place = Place(**request_body)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400)
    request_body = request.get_json()
    for key, value in request_body.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def search_for_places():
    """Shows all places in an city  or in state"""
    if not request.json:
        abort(400)
    if len(request.get_json()) < 1:
        return jsonify(
            [place_to_dict() for place in storage.all("Place").values()])
    request_body = request.get_json()
    amenities = request_body.get("amenities", [])
    places = []
    for key, values in request_body.items():
        if key == "states":
            for state_id in values:
                cities_id = [city.id for city in storage.all("City").values()
                             if state_id == city.state_id]
            places.extend([place.to_dict()
                           for place in storage.all("Place").values()
                           if place.city_id in cities_id])
        if key == "cities":
            places.extend([place.to_dict()
                           for place in storage.all("Place").values()
                           if place.city_id in values])
    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in place.amenities
                   for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places
    return jsonify(places)

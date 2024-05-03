#!/usr/bin/python3
"""This module """


from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route(
    "places/<place_id>/reviews", strict_slashes=False)
def show_place_reviws(place_id):
    """show all the reviews by place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict()
                    for review in storage.all("Review").values()
                    if place_id == review.place_id])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def show_review(review_id):
    """ Show a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    request_body = request.get_json()
    if "user_id" not in request_body:
        return jsonify(error="Missing user_id"), 400
    if "text" not in request_body:
        return jsonify(error="Missing text"), 400
    user_id = request_body["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    request_body["place_id"] = place_id
    new_review = Review(**request_body)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    request_body = request.get_json()
    for key, value in request_body.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

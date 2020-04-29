#!/usr/bin/python3
"""Review request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def review_by_place(place_id=None):
    """GET cities by state request"""
    review_list = []
    state = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in place.review:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """GET request"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """DELETE request"""
    review = storage.get(Review, review_id)
    if not user:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_users():
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    if not storage.get('User', request.get_json()['user_id']):
        abort(404)
    new = Review(**info)
    new.place_id = place_id
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def put_place(review_id):
    """PUT request"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

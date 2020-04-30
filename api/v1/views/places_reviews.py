#!/usr/bin/python3
"""Reviews request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """GET reviews by place request"""
    reviews_list = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviews(review_id):
    """GET request"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_reviews(review_id):
    """DELETE request"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def post_reviews(place_id):
    """POST request"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "user_id" not in info:
        abort(400, "Missing user_id")
    if "text" not in info:
        abort(400, "Missing text")
    user = storage.get(User, info["user_id"])
    if not user:
        abort(404)
    new = Review(**info)
    new.place_id = place.id
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def put_reviews(review_id):
    """PUT request"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id",
                       "user_id",
                       "place_id",
                       "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

#!/usr/bin/python3
"""Amenity request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities(amenity_id=None):
    """GET request"""
    amenities_list = []
    if not amenity_id:
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """DELETE request"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenities():
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "name" not in info:
        abort(400, "Missing name")
    new = Amenity(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def put_amenities(amenity_id):
    """PUT request"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200

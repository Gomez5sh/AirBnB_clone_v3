#!/usr/bin/python3
"""Place request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """GET places by city request"""
    places_list = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_places(place_id):
    """GET request"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_places(place_id):
    """DELETE request"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def post_places(city_id):
    """POST request"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "user_id" not in info:
        abort(400, "Missing user_id")
    if "name" not in info:
        abort(400, "Missing name")
    user = storage.get(User, info["user_id"])
    if not user:
        abort(404)
    new = Place(**info)
    new.city_id = city.id
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_places(place_id):
    """PUT request"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

#!/usr/bin/python3
"""Citys request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
@app_views.route("/cities", methods=["GET"], strict_slashes=False)
def get_cities(city_id=None):
    """GET request"""
    City_list = []
    if not state_id:
        states = storage.all(State).values()
        for city in states.city:
            City_list.append(city.to_dict())
        return jsonify(states_list)
    else:
        city = storage.get(City, city_id)
        if not state:
            abort(404)
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>/",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_cities(city_id):
    """DELETE request"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "name" not in info:
        abort(400, "Missing name")
    new = State(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """PUT request"""
    state = storage.get(City, city_id)
    if not city:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

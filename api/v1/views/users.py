#!/usr/bin/python3
"""User request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users(user_id=None):
    """GET request"""
    user_list = []
    if not user_id:
        users = storage.all(User).values()
        for user in user:
            user_list.append(user.to_dict())
        return jsonify(user_list)
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_users(user_id):
    """DELETE request"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_users():
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "name" not in info:
        abort(400, "Missing name")
    new = User(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_users(user_id):
    """PUT request"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

#!/usr/bin/python3
"""Create a new view for State objects
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_all_states(state_id=None):
    """Retrieves the list of all State
    """
    n = []
    all_states = storage.all('State')
    for i in all_states.values():
        n.append(i.to_dict())
    return jsonify(n)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Retrieves a State object
    """
    state_iter = storage.get("State", state_id)
    if state_iter is None:
        abort(404)
    return jsonify(state_iter.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    """Deletes a State object
    """
    state_iter = storage.get("State", state_id)
    if state_iter is None:
        abort(404)
    storage.delete(state_iter)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Creates a State: POST
    """
    if not request.get_json():
        abort(404, "Not a JSON")

    if 'name' not in request.get_json():
        abort(404, "Missing name")

    data = request.get_json()
    temp = State(**data)
    temp.save()
    return make_response(jsonify(temp.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """State object: PUT
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)

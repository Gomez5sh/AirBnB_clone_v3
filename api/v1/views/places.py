#!/usr/bin/python3
"""place request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
@app_views.route("/places/", methods=["GET"], strict_slashes=False)
def get_places(place_id=None):
    """GET request"""
    place_list = []
    if not place_id:
        places = storage.all(Place).values()
        for place in places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """DELETE request"""
    place = storage.get(Place, place_id)
    if not user:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/place", methods=["POST"], strict_slashes=False)
def post_place():
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if not storage.get('User', request.get_json()['user_id']):
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    new = Place(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/place/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """PUT request"""
    place  = storage.get(User, user_id)
    if not place:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

@app_views.route('/places_search', methods=['POST'])
def psearch():

    headers = request.headers.get('Content-Type')
    if headers != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        return jsonify([places.to_dict() for
                        places in storage.all('Place').values()])

    res = []
    places = []
    amenities = []
    obj = request.get_json()

    for k, v in obj.items():
        if k == 'states':
            for item in v:
                state_obj = storage.get('State', item)
                for city in state_obj.cities:
                    res.append(city.id)

    for k, v in obj.items():
        if k == 'cities':
            for item in v:
                if item not in res:
                    res.append(item)


    for k, v in obj.items():
        if k == 'amenities':
            for item in v:
                if item not in res:
                    amenities.append(item)


    for place in storage.all('Place').values():
        if place.city_id in res:
            places.append(place.id)


    if places == [] and amenities != []:
        remove = []
        res = []
        places = [place.id for place in storage.all('Place').values()]
        for place in places:
            obj = storage.get('Place', place)
            for amen in obj.amenities:
                if amen.id not in amenities:
                    if place not in remove:
                        remove.append(place)
        for place in places:
            if place not in remove:
                res.append(place)
        return jsonify([storage.get('Place', obj).to_dict()
                        for obj in res])

    if amenities != []:
        for place in places:
            obj = storage.get('Place', place)
            for amenity in amenities:
                if amenity not in obj.amenities:
                    places.remove(place)

    return jsonify([storage.get('Place', id).to_dict() for id in places])

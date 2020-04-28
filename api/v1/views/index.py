#!/usr/bin/python3
"""Routes"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats", strict_slashes=False)
def stats():
    """Stats"""
    classes = [Amenity, City, Place, Review, State, User]
    keys = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats_count = {}
    for idx in range(len(clases)):
        stats_count[keys[idx]] = storage.count(classes[idx])
    return jsonify(stats_count)

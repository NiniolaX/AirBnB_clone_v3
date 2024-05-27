#!/usr/bin/python3
""" Contains a route '/status' that returns the status of the api """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def return_status():
    """ Returns the status of the api """
    status = jsonify({"status": "OK"})
    return status


@app_views.route('/stats')
def return_stats():
    """ Returns the number of each object by type """
    from models import storage
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity
    models = {"amenities": Amenity, "cities": City, "places": Place,
              "reviews": Review, "states": State, "users": User}
    stats = {}
    for key, value in models.items():
        stats[key] = storage.count(value)

    return jsonify(stats)

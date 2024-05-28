#!/usr/bin/python3
""" Defines a new view for handling all default RESTful API actions on Place
objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """ Retrieves list of all Place objects associated with a given city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = storage.all(Place).values()
    places_in_json = []
    for place in places:
        if place.city_id == city_id:
            places_in_json.append(place.to_dict())
    return jsonify(places_in_json)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object in a city """
    city = storage.get(City, city_id)
    # Check that city_id is linked to a City object
    if not city:
        abort(404)

    # Deserialize request data
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    # Check that user_id was passed and is linked to a User object
    if "user_id" not in request_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    # Check that name was passed
    if "name" not in request_data:
        abort(400, description="Missing name")

    new_place = Place(city_id=city_id, **request_data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200

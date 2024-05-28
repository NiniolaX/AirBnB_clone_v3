#!/usr/bin/python3
"""
Defines a new view for handling all default RESTful API actions on City
objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ Retrieves list of all City objects of a state """
    # Check that state_id is linked to a State object
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = state.cities
    cities_in_json = []
    for city in cities:
        cities_in_json.append(city.to_dict())
    return jsonify(cities_in_json)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a new State object """
    # Check that state_id is linked to a State object
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if "name" not in request_data:
        abort(400, description="Missing name")

    new_city = City(state_id=state_id, **request_data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    # Check that city_id is linked to a City object
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200

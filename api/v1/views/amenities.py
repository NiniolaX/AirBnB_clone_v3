#!/usr/bin/python3
"""
Defines a new view for handling all default RESTful API actions on Amenity
objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ Retrieves list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    amenities_in_json = []
    for amenity in amenities:
        amenities_in_json.append(amenity.to_dict())
    return jsonify(amenities_in_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object """
#    if not request.is_json:
#        abort(400, description="Not a JSON")
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if "name" not in request_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**request_data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200

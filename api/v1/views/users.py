#!/usr/bin/python3
"""
Defines a new view for handling all default RESTful API actions on User
objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ Retrieves list of all User objects """
    users = storage.all(User).values()
    users_in_json = []
    for user in users:
        users_in_json.append(user.to_dict())
    return jsonify(users_in_json)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a new User object """
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if "email" not in request_data:
        abort(400, description="Missing email")
    if "password" not in request_data:
        abort(400, description="Missing password")

    new_user = User(**request_data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200

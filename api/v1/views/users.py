#!/usr/bin/python3
"""Defines a new view for handling all default RESTful API actions on User
objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


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
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "email" not in request_data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request_data:
        return make_response(jsonify({"error": "Missing password"}), 400)

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
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200

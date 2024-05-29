#!/usr/bin/python3
""" Defines a new view for handling all default RESTful API actions on Review
objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ Retrieves list of all Review objects associated with a given place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = storage.all(Review).values()
    reviews_in_json = []
    for review in reviews:
        if review.place_id == place_id:
            reviews_in_json.append(review.to_dict())
    return jsonify(reviews_in_json)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object in a place """
    place = storage.get(Place, place_id)
    # Check that place_id is linked to a Place object
    if not place:
        abort(404)

    # Deserialize request data
    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    # Check that user_id was passed and is linked to a User object
    if "user_id" not in request_data:
        return make_response({"error": "Missing user_id"}, 400)
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    # Check that text was passed
    if "text" not in request_data:
        return make_response({"error": "Missing text"}, 400)

    # Create new place object
    request_data['place_id'] = place_id
    new_review = Review(**request_data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    for key, value in request_data.items():
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200

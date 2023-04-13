#!/usr/bin/python3
"""
Places_reviews file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import models
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''Retrieves all reviews objects of a place'''
    place = models.storage.get(Place, place_id)
    reviewList = []
    if not place:
        abort(404)
    for review in place.reviews:
        reviewList.append(review.to_dict())
    return jsonify(reviewList)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    '''retrieves a review given its id'''
    review = models.storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    '''deletes a review given its id'''
    review = models.storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        models.storage.delete(review)
        models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    '''Returns the new Review with the status code 201'''
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)

    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'text' not in dictionary:
        return jsonify({'error': 'Missing text'}), 400
    if 'user_id' not in dictionary:
        return jsonify({'error': 'Missing user_id'}), 400

    user = models.storage.get(User, dictionary['user_id'])
    if not user:
        abort(404)

    else:
        newReview = Review(**dictionary)
        models.storage.save()
        return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review given its id"""
    """We search in the db for the given review"""
    review = models.storage.get(Review, review_id)
    if not review:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    """We update the instance ignoring its id, createdat and updatedat"""
    for key, value in dictionary.items():
        if key not in ['id', 'user_id', 'place_id' 'created_at', 'updated_at']:
            setattr(review, key, value)
    models.storage.save()
    return jsonify(review.to_dict()), 200

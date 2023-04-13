#!/usr/bin/python3
"""
Amenity file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import models
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''Retrieves the list of all amenities objects'''
    allAmenities = models.storage.all(Amenity).values()
    amenityList = []
    for amenity in allAmenities:
        amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    '''retrieves an amenity given its id'''
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    '''deletes an amenity given its id'''
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        models.storage.delete(state)
        models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenites', methods=['POST'], strict_slashes=False)
def post_amenities():
    '''Returns the new Amenity with the status code 201'''
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    elif 'name' not in dictionary:
        return jsonify({'error': 'Missing name'}), 400
    else:
        newAmenity = Amenity(**dictionary)
        models.storage.save()
        return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(amenity_id):
    """Updates an amenity given its id"""
    """We search in the db for the given amenity"""
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    """We update the instance ignoring its id, createdat and updatedat"""
    for key, value in dictionary.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    models.storage.save()
    return jsonify(amenity.to_dict()), 200

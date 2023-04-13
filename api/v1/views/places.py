#!/usr/bin/python3
"""
Places file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import models
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''Retrieves all places objects of a city'''
    city = models.storage.get(City, city_id)
    placesList = []
    if not city:
        abort(404)
    for place in city.places:
        placesList.append(place.to_dict())
    return jsonify(placesList)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    '''retrieves a place given its id'''
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    '''deletes a place given its id'''
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        models.storage.delete(place)
        models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    '''Returns the new place with the status code 201'''
    city = models.storage.get(City, city_id)
    if not city:
        abort(404)

    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in dictionary:
        return jsonify({'error': 'Missing name'}), 400

    if 'user_id' not in dictionary:
        return jsonify({'error': 'Missing user_id'}), 400
    user = models.storage.get(User, dictionary['user_id'])
    if not user:
        abort(404)

    else:
        newPlace = Place(**dictionary)
        models.storage.save()
        return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place given its id"""
    """We search in the db for the given place"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    """We update the instance ignoring its id, createdat and updatedat"""
    for key, value in dictionary.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    models.storage.save()
    return jsonify(place.to_dict()), 200

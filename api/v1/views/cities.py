#!/usr/bin/python3
"""
City file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import models
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    '''Retrieves all city objects of a state'''
    state = models.storage.get(State, state_id)
    cityList = []
    if not state:
        abort(404)
    for city in state.cities:
        cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    '''retrieves a city given its id'''
    city = models.storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(city_id):
    '''deletes a city given its id'''
    city = models.storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        models.storage.delete(city)
        models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_cities():
    '''Returns the new city with the status code 201'''
    state = models.storage.get(State, state_id)
    if not state:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    elif 'name' not in dictionary:
        return jsonify({'error': 'Missing name'}), 400
    else:
        newCity = City(**dictionary)
        newCity.state_id = state_id
        models.storage.save()
        return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City given its id"""
    """We search in the db for the given city"""
    city = models.storage.get(City, city_id)
    if not city:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    """We update the instance ignoring its id, createdat and updatedat"""
    for key, value in dictionary.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    models.storage.save()
    return jsonify(city.to_dict()), 200

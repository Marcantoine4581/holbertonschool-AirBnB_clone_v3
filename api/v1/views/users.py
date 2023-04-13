#!/usr/bin/python3
"""
Users file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import models
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''Retrieves the list of all User objects'''
    allUsers = models.storage.all(User).values()
    usersList = []
    for user in allUsers:
        usersList.append(state.to_dict())
    return jsonify(usersList)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    '''retrieves a User given its id'''
    user = models.storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_id(user_id):
    '''deletes a user given its id'''
    user = models.storage.get(User, user_id)
    if not user:
        abort(404)
    else:
        models.storage.delete(user)
        models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    '''Returns the new User with the status code 201'''
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    elif 'email' not in dictionary:
        return jsonify({'error': 'Missing email'}), 400
    elif 'password' not in dictionary:
        return jsonify({'error': 'Missing password'}), 400
    else:
        newUser = User(**dictionary)
        models.storage.save()
        return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """Updates a User given its id"""
    """We search in the db for the given state"""
    user = models.storage.get(User, user_id)
    if not user:
        abort(404)
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    """We update the instance ignoring its id, createdat and updatedat"""
    for key, value in dictionary.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    models.storage.save()
    return jsonify(user.to_dict()), 200

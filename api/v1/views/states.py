#!/usr/bin/python3
"""
State file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import models
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Retrieves the list of all State objects'''
    allStates = models.storage.all(State).values()
    statesList = []
    for state in allStates:
        statesList.append(state.to_dict())
    return jsonify(statesList)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    '''retrieves a state given its id'''
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    '''deletes a state given its id'''
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        obj = State + '.' + state_id
        models.storage.delete(obj)
        models.storage.save()
    return state, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    '''Returns the new State with the status code 201'''
    dictionary = request.get_json()
    if not dictionary:
        return jsonify({'error': 'Not a JSON'}), 400

    elif 'name' not in dictionary:
        return jsonify({'error': 'Missing name'}), 400
    #fonction à terminer

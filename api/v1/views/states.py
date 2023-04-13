#!/usr/bin/python3
"""
State file
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import 
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """cette fonction permet de récupérer une instance
    spécifique avec un id pour la retrouver."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, {'error': 'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'error': 'Missing name'})

    data = request.get_json()
    # ** permet de faire passer args
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    récupérer un objet d'état spécifique
    à partir de son ID et lui changer valeur
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    non = ['id', 'created_at', 'updated_at']

    # données requête récupérées
    data = request.get_json()

    for key, value in data.items():
        if key not in non:
            setattr(state, key, value)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)

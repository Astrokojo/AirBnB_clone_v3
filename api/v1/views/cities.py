#!/usr/bin/python3
"""Defines API endpoints for City objects"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, state, city

City = city.City
State = state.State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
    strict_slashes=False)


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves all cities associated with a state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a specific city by its ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city by its ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new city"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city by its ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    except Exception as e:
        abort(400, f'Error parsing JSON: {str(e)}')


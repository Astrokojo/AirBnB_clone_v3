#!/usr/bin/python3
"""A Flask route that returns json status response of amenities module."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, amenity

Amenity = amenity.Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Returns all amenities object in json format"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a specific amenity by its ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """This Deletes a specific amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    # if the amenity is not found, raise a 404 error
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """this create a new amenity object"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity object with the given id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    except Exception as e:
        abort(400, f'Error parsing JSON: {str(e)}')

#!/usr/bin/python3
"""Test for api/v1/views/amenities.py"""
import unittest
from flask import json
from api.v1.app import app
from models import storage, amenity

Amenity = amenity.Amenity

class TestAmenitiesAPI(unittest.TestCase):
    """
    A Unittest to test the ameinities API
    """
    def setUp(self):
        # Initialize Flask app test Amenity API
        self.app = app.test_client()
        self.amenity_data = {'name':'Test Amenity'}
        self.amenity = Amenity(**self.amenity_data)
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        # Reset the database after each test
        storage.delete(self.amenity)
        storage.save()

    def test_get_amenities(self):
        """Test case for retrieving all amenities"""
        response = self.app.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

    def test_get_amenity(self):
        # Test case for retrieving a specific amenity
        amenity = Amenity(name="Test Amenity")
        storage.new(amenity)
        storage.save()
        response = self.app.get(f"/api/v1/amenities/{amenity.id}/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], amenity.id)
        # Test case for retrieving a non-existent amenity
        response = self.app.get('/api/v1/amenities/1000/')
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        # Test case for deleting an existing amenity
        amenity = Amenity(name="Test Amenity")
        storage.new(amenity)
        storage.save()
        response = self.app.delete(f'/api/v1/amenities/{amenity.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(Amenity, amenity.id), None)

        # Test Case for deleting a non-existent amenity
        response = self.app.delete('/api/v1/amenities/1000/')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        # Test case for creating a new amenity
        data = {'name': 'New Amenity'}
        response = self.app.post('/api/v1/amenities/', json=data)
        self.assertEqual(response.status_code, 201)
        amenity_id = json.loads(response.get_data(as_text=True))['id']
        self.assertTrue(storage.get(Amenity, amenity_id))
        # Test case for creating an amenity with missing data
        response = self.app.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

        # Test case for creating an amenity with an invalid json
        response = self.app.post('/api/v1/amenities/', json='invalid json')
        self.assertEqual(response.status_code, 400)

    def test_update_amenities(self):
        # Test case for updating an existing amenity
        amenity = Amenity(name="Test Amenity Original")
        storage.new(amenity)
        storage.save()
        data = {'name': 'Updated Amenity'}
        response = self.app.put(f'/api/v1/amenities/{amenity.id}/', json=data)
        self.assertEqual(response.status_code, 200)
        updated_amenity = storage.get(Amenity, amenity.id)
        self.assertEqual(updated_amenity.name, 'Updated Amenity')
        # Test case for updating a non-existent amenity
        response = self.app.put('/api/v1/amenities/1000/', json=data)
        self.assertEqual(response.status_code, 404)

        # Test case for updating an amenity with an invalid json
        response = self.app.put(f'/api/v1/amenities/{amenity.id}/', json='invalid json')
        self.assertEqual(response.status_code, 400)

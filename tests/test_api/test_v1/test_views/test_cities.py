#!/usr/bin/python3
"""Test for api/v1/views/cities.py"""
import unittest
from flask import json
from api.v1.app import app
from models import storage, state, city

State = state.State
City = city.City

class TestCitiesAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.state = State(name="Test State")
        self.city = City(name="Test City", state_id=self.state.id)
        storage.new(self.state)
        storage.new(self.city)
        storage.save()

    def tearDown(self):
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()

    def test_get_cities(self):
        response = self.app.get('/api/v1/states/{}/cities'.format(self.state.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

    def test_get_city(self):
        response = self.app.get('/api/v1/cities/{}'.format(self.city.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], self.city.id)

    def test_delete_city(self):
        response = self.app.delete('/api/v1/cities/{}'.format(self.city.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(storage.get('City', self.city.id))

    def test_create_city(self):
        data = {'name': 'New City', 'state_id': self.state.id}
        response = self.app.post('/api/v1/states/{}/cities'.format(self.state.id), json=data)
        self.assertEqual(response.status_code, 201)
        city_id = json.loads(response.get_data(as_text=True))['id']
        self.assertTrue(storage.get('City', city_id))
        # Test case for creating a city with missing data
        response = self.app.post('/api/v1/states/{}/cities'.format(self.state.id), json={})
        self.assertEqual(response.status_code, 400)
        # Test case for creating a city with invalid JSON
        response = self.app.post('/api/v1/states/{}/cities'.format(self.state.id), json='invalid json')
        self.assertEqual(response.status_code, 400)

    def test_update_city(self):
        data = {'name': 'Updated City'}
        response = self.app.put('/api/v1/cities/{}'.format(self.city.id), json=data)
        self.assertEqual(response.status_code, 200)
        updated_city = storage.get('City', self.city.id)
        self.assertEqual(updated_city.name, 'Updated City')
        # Test case for updating a non-existent city
        response = self.app.put('/api/v1/cities/1000', json=data)
        self.assertEqual(response.status_code, 404)
        # Test case for updating a city with invalid JSON
        response = self.app.put('/api/v1/cities/{}'.format(self.city.id), json='invalid json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

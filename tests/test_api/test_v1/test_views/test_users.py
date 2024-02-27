#!/usr/bin/python3
""" Test for api/v1/views/users.py """
import unittest
from flask import json
from api.v1.app import app
from models import storage, user

User = user.User    # User class


class TestUsersAPI(unittest.TestCase):
    """ Test for users API """

    def setUp(self):
        """ Initialize Flask app for testing users API """
        self.app = app.test_client()
        self.user_data = {'email': 'name@example.com', 'password': 'testpass'}
        self.user = User(**self.user_data)
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        """ Reset the database after each test """
        storage.delete(self.user)
        storage.save()

    def test_get_users(self):
        """ Test case for retrieving all users """
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

    def test_get_user(self):
        """ Test case for retrieving a specific user """
        user = User(name="Username")
        storage.new(user)
        storage.save()
        response = self.app.get(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], user.id)

        # Test case for retrieving a non-existing user
        response = self.app.get('/api/v1/users/1000')
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        """ Test case for deleting an existing user """
        user = User(name="Test User")
        storage.new(user)
        storage.save()
        response = self.app.delete(f'/api/v1/users/{user.id}')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get('User', user.id), None)

        # Test case for deleting a non-existing user
        response = self.app.delete('/api/v1/users/1000')
        self.assertEqual(response.status_code, 404)



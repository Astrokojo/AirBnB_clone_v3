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
        # Ensure the user is deleted from storage if it exists
        user = storage.get(User, self.user.id)
        if user:
            storage.delete(user)
            storage.save()

    def test_get_users(self):
        """ Test case for retrieving all users """
        # Ensure there's at least one user in storage
        response = self.app.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)  # Ensure the list is not empty

    def test_get_user(self):
        """ Test case for retrieving a specific user """
        # Use the user created in setUp
        response = self.app.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], str(self.user.id))  # Ensure the IDs match

    def test_delete_user(self):
        """ Test case for deleting an existing user """
        # Use the user created in setUp
        response = self.app.delete(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        # Verify the user is no longer in storage
        self.assertIsNone(storage.get(User, self.user.id))


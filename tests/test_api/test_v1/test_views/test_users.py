#!/usr/bin/python3
""" Tests the user view of the API """
import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User
from os import getenv


class UserApiTestCase(unittest.TestCase):
    """ Tests the user view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.app = app.test_client()
        self.app.testing = True

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize storage
        storage.reload()

        # Create test user object
        self.user = User(email='test01@gmail.com', password='0123')
        self.user.save()

    def tearDown(self):
        """ Cleans up test environment """
        # Delete test user object
        self.user.delete()
        storage.save()

        # Close storage
        storage.close()
        self.app_context.pop()

    def test_get_users(self):
        """ Test GET /api/v1/users endpoint """
        response = self.app.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that user object exists in data returned
        self.assertIn(self.user.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["Amenity", "City", "State", "Place", "Review"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_user(self):
        """ Test GET /api/v1/users/<user_id> endpoint """
        response = self.app.get(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['id'], self.user.id)
        self.assertEqual(data_returned['email'], 'test01@gmail.com')

    def test_delete_user(self):
        """ Test DELETE /api/v1/users/<user_id> endpoint """
        response = self.app.delete(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_user(self):
        """ Test POST /api/v1/users/ endpoint """
        # Test create user with email and password
        user_data = {'email': 'test02@gmail.com', 'password': '123'}
        response = self.app.post('/api/v1/users/',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data_returned = json.loads(response.data)
        self.assertIn('id', data_returned)
        self.assertEqual(data_returned['email'], 'test02@gmail.com')

        # Check that new object is in storage
        user_key = f"User.{data_returned['id']}"
        self.assertIn(user_key, storage.all(User))

        # Test create user without email
        response = self.app.post('/api/v1/users/',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        """ Test PUT /api/v1/user/<user_id>' endpoint """
        response = self.app.put(f'/api/v1/users/{self.user.id}',
                                data=json.dumps({'name': 'Updated User'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['name'], 'Updated User')

        # Check that update is visible in storage
        user = storage.get(User, self.user.id)
        self.assertEqual(user.name, 'Updated User')


if __name__ == '__main__':
    unittest.main()

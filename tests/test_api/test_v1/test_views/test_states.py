#!/usr/bin/python3
""" Tests the state view of the API """
import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State
from os import getenv


class StateApiTestCase(unittest.TestCase):
    """ Tests the state view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.app = app.test_client()
        self.app.testing = True

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize storage
        storage.reload()

        # Create test state object
        self.state = State(name='Test State')
        self.state.save()

    def tearDown(self):
        """ Cleans up test environment """
        # Delete test state object
        self.state.delete()
        storage.save()

        # Close storage
        storage.close()
        self.app_context.pop()

    def test_get_states(self):
        """ Test GET /api/v1/states endpoint """
        response = self.app.get('/api/v1/states/')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        print(data_returned)
        self.assertEqual(len(data_returned), 1)
        self.assertEqual(data_returned[0]['id'], self.state.id)
        self.assertEqual(data_returned[0]['name'], 'Test State')

    def test_get_state(self):
        """ Test GET /api/v1/states/<state_id> endpoint """
        response = self.app.get(f'/api/v1/states/{self.state.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['id'], self.state.id)
        self.assertEqual(data_returned['name'], 'Test State')

    def test_delete_state(self):
        """ Test DELETE /api/v1/states/<state_id> endpoint """
        response = self.app.delete(f'/api/v1/states/{self.state.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_state(self):
        """ Test POST /api/v1/states/ endpoint """
        response = self.app.post('/api/v1/states/',
                                 data=json.dumps({'name': 'New State'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data_returned = json.loads(response.data)
        self.assertIn('id', data_returned)
        self.assertEqual(data_returned['name'], 'New State')

        # Check that new object is in storage
        state_key = f"State.{data_returned['id']}"
        self.assertIn(state_key, storage.all(State))

    def test_update_state(self):
        """ Test PUT /api/v1/state/<state_id>' endpoint """
        response = self.app.put(f'/api/v1/states/{self.state.id}',
                                data=json.dumps({'name': 'Updated State'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['name'], 'Updated State')

        # Check that update is visible in storage
        state = storage.get(State, self.state.id)
        self.assertEqual(state.name, 'Updated State')


if __name__ == '__main__':
    unittest.main()

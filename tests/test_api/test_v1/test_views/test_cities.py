#!/usr/bin/python3
""" Tests the cities view of the API """
import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State
from models.city import City
from os import getenv


class CityApiTestCase(unittest.TestCase):
    """ Tests the city view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.app = app.test_client()
        self.app.testing = True

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize storage
        storage.reload()

        # Create test objects
        self.state = State(name='Test State')
        self.state.save()
        self.city = City(name='Test City', state_id=self.state.id)
        self.city.save()

    def tearDown(self):
        """ Cleans up test environment """
        # Delete test state object
        self.state.delete()
        self.city.delete()
        storage.save()

        # Close storage
        storage.close()
        self.app_context.pop()

    def test_get_cities(self):
        """ Test GET /api/v1/states/<state_id>/cities endpoint """
        response = self.app.get(f'/api/v1/states/{self.state.id}/cities')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        print(data_returned)
        self.assertEqual(len(data_returned), 1)
        self.assertEqual(data_returned[0]['id'], self.city.id)
        self.assertEqual(data_returned[0]['name'], 'Test City')

    def test_get_city(self):
        """ Test GET /api/v1/cities/<city_id> endpoint """
        response = self.app.get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['id'], self.city.id)
        self.assertEqual(data_returned['name'], 'Test City')

    def test_delete_city(self):
        """ Test DELETE /api/v1/cities/<city_id> endpoint """
        response = self.app.delete(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_city(self):
        """ Test POST /api/v1/<state_id>/cities endpoint """
        response = self.app.post(f'/api/v1/{self.state.id}/cities',
                                 data=json.dumps({'name': 'New City'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data_returned = json.loads(response.data)
        self.assertIn('id', data_returned)
        self.assertEqual(data_returned['name'], 'New City')

        # Check that new object is in storage
        city_key = f"City.{data_returned['id']}"
        self.assertIn(city_key, storage.all(City))

    def test_update_state(self):
        """ Test PUT /api/v1/cities/<city_id>' endpoint """
        response = self.app.put(f'/api/v1/cities/{self.city.id}',
                                data=json.dumps({'name': 'Updated City'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['name'], 'Updated City')

        # Check that update is visible in storage
        city = storage.get(City, self.city.id)
        self.assertEqual(city.name, 'Updated City')


if __name__ == '__main__':
    unittest.main()

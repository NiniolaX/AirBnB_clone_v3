#!/usr/bin/python3
""" Tests the amenity view of the API """
import unittest
import json
from api.v1.app import app
from models import storage
from models.amenity import Amenity
from os import getenv


class AmenityApiTestCase(unittest.TestCase):
    """ Tests the amenity view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.app = app.test_client()
        self.app.testing = True

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize storage
        storage.reload()

        # Create test amenity object
        self.amenity = Amenity(name='Test Amenity')
        self.amenity.save()

    def tearDown(self):
        """ Cleans up test environment """
        # Delete test amenity object
        self.amenity.delete()
        storage.save()

        # Close storage
        storage.close()
        self.app_context.pop()

    def test_get_amenities(self):
        """ Test GET /api/v1/amenities endpoint """
        response = self.app.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that amenity object exists in data returned
        self.assertIn(self.amenity.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["State", "City", "User", "Place", "Review"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_amenity(self):
        """ Test GET /api/v1/amenities/<amenity_id> endpoint """
        response = self.app.get(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['id'], self.amenity.id)
        self.assertEqual(data_returned['name'], 'Test Amenity')

    def test_delete_amenity(self):
        """ Test DELETE /api/v1/amenities/<amenity_id> endpoint """
        response = self.app.delete(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_amenity(self):
        """ Test POST /api/v1/amenities/ endpoint """
        response = self.app.post('/api/v1/amenities/',
                                 data=json.dumps({'name': 'New Amenity'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data_returned = json.loads(response.data)
        self.assertIn('id', data_returned)
        self.assertEqual(data_returned['name'], 'New Amenity')

        # Check that new object is in storage
        amenity_key = f"Amenity.{data_returned['id']}"
        self.assertIn(amenity_key, storage.all(Amenity))

    def test_update_amenity(self):
        """ Test PUT /api/v1/amenity/<amenity_id>' endpoint """
        response = self.app.put(f'/api/v1/amenities/{self.amenity.id}',
                                data=json.dumps({'name': 'Updated Amenity'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned['name'], 'Updated Amenity')

        # Check that update is visible in storage
        amenity = storage.get(Amenity, self.amenity.id)
        self.assertEqual(amenity.name, 'Updated Amenity')


if __name__ == '__main__':
    unittest.main()

import unittest
import os
import json
from flask import Flask
from app.app import create_app
from models.content import content_data, Content


class EntryTestCase(unittest.TestCase):
    """Test Entry content in app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.data = {"Date": "01/01/18", "Content": "I had fun at the zoo"}

    def test_api_can_get_all_entries(self):
        """Test API can GET all entries """
        response = self.client.post(
            'api/v1/user/entries',
            data=json.dumps(self.data),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get('api/v1/user/entries')
        self.assertEqual(response.status_code, 200)

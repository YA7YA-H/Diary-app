import unittest
import os
import json
from flask import Flask
from app.app import create_app


class EntryTestCase(unittest.TestCase):
    """Test Entry content in app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user = {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "John_Doe@example.com",
            "Password": "its26uv3nf"
        }

    def test_user_signup(self):
        """Test user registration"""

        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user),
            content_type="application/json")

        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Successfully registered.')
        self.assertEqual(response.status_code, 201)
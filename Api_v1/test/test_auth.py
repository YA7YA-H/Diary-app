import unittest
import os
import json
from flask import Flask
from Api_v1.app.app import create_app
from Api_v1.app.models.user import User
from Api_v1.app.app import db


class AuthTestCase(unittest.TestCase):
    """Test Entry content in app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_registration = {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "John_Doe@example.com",
            "Password": "its26uv3nf"
        }

    def tearDown(self):
        db.drop_database()
        db.create_tables_entry()
        db.create_tables_user()

    def register_user(self,
                      last_name="Doe",
                      first_name="John",
                      email="John_Doe@example.com",
                      password="its26uv3nf"):
        """signup helper"""
        user_data = {
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "Password": password
        }
        return self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(user_data),
            content_type="application/json")

    def sign_in_user(self, email="John_Doe@example.com",
                     password="its26uv3nf"):
        """A login helper method"""
        user_data = {"Email": email, "Password": password}
        return self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(user_data),
            content_type="application/json")

    def test_encode_auth_token(self):
        user = User(
            firstname="test",
            lastname="tester",
            email='test@test.com',
            password='test123')
        user.create()
        auth_token = user.encode_auth_token(user.email)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_signup_already_user_existing_email(self):
        """Test user registration"""
        self.register_user()
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"], "Email already exist")
        self.assertEqual(response.status_code, 401)

    def test_signup_new_user(self):
        """Test user registration"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "newuser2@example.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)

        self.assertEqual(result["message"], 'Successfully registered.')
        self.assertEqual(response.status_code, 201)

    def test_signup_names_less_than_two_char(self):
        """Test user signups name with less than two characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "J",
                "LastName": "Do",
                "Email": "fakeDoe@example.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"], "Names should be more than 2 ")
        self.assertEqual(response.status_code, 400)

    def test_signup_names_invalid_char(self):
        """Test user signups name with invalid characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "!!!!!!!!!",
                "LastName": "$$$$$$$$$$$$",
                "Email": "character@example.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Invalid character in your name(s)")
        self.assertEqual(response.status_code, 400)

    def test_signup_password_less_than_six_char(self):
        """Test user signups  with less than six characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "testpassword@example.com",
                "Password": "abc"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Password should be more than 6 character ")
        self.assertEqual(response.status_code, 400)

    def test_signup_email_invalid_char(self):
        """Test user signups email with invalid characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "look!!!!!!!!@invalid.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"], "Invalid character in your email ")
        self.assertEqual(response.status_code, 400)

    def test_signup_email_less_than_four_char(self):
        """Test user signups email with less than four characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": ".co",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Email should be more than 4 character ")
        self.assertEqual(response.status_code, 400)

    #LOGIN TESTS
    def test_api_invalid_Login(self):
        """Test for invalid password in signin endpoint"""

        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                "Email": "John_Doe@example.com",
                "Password": "fakepaswd"
            }),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["Message"], 'Failed try again')
        self.assertEqual(response.status_code, 401)

    def test_api_user_login_successfully(self):
        """Test user signin successfully"""
        self.register_user()
        result = self.sign_in_user()
        self.assertEqual(result.status_code, 201)

    # def test_valid_logout(self):
    #     """Test for logout before token expires """
    #     self.register_user()
    #     login = self.sign_in_user()

    #     #entries
    #     access_token = json.loads(login.data.decode())['auth_token']
    #     # valid token logout
    #     response = self.client.post(
    #         '/api/v1/auth/logout',
    #         content_type="application/json",
    #         headers=dict(access_token=access_token))
    #     self.assertEqual(response.status_code, 200)

    # def test_invalid_logout(self):
    #     """Test for logout before token expires """
    #     self.register_user()
    #     self.sign_in_user()

    #     # invalid token logout
    #     response = self.client.post(
    #         '/api/v1/auth/logout', content_type="application/json")
    #     self.assertEqual(response.status_code, 401)

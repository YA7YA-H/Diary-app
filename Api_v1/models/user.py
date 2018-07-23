user_data = {}
from flask_bcrypt import Bcrypt
import jwt
import datetime
import os


class User:
    """Class for user"""

    def __init__(self, firstname, lastname, email, password):
        global user_data
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def create(self):
        user = {
            self.email: {
                "FirstName": self.firstname,
                "LastName": self.lastname,
                "Email": self.email,
                "Password": self.password_hash
            },
        }
        return user_data.update(user)

    @classmethod
    def encode_auth_token(cls, user_id):
        """
        Generates the Auth Token
        :return: string
        """

        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                str(user_id)
            }
            return jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')
        except Exception as e:
            return str(e)

user_data = {}
from flask_bcrypt import Bcrypt
import jwt
import datetime
from Api_v1.app.app import db
import os


class User:
    """Class for a user"""

    def __init__(self, firstname, lastname, email, password):
        global user_data
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def create(self):
        db.add_new_user(self.firstname, self.lastname, self.email, self.password_hash)

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

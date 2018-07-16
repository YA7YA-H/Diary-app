from flask_restplus import Resource, Namespace, fields
from flask import request
from models.user import user_data, User

auth_namespace = Namespace(
    'auth', description="Handle Authentification Related Operation")

registration_model = auth_namespace.model(
    "Registration", {
        "FirstName":
        fields.String(
            required=True, description='Your First Name', example='John'),
        "LastName":
        fields.String(
            required=True, description='Your Last Name', example='Doe'),
        "Email":
        fields.String(
            required=True,
            description='your email accounts',
            example='John_Doe@example.com'),
        "Password":
        fields.String(
            required=True,
            description='Your secret password',
            example='its26uv3nf')
    })


@auth_namespace.route("/signup")
class Signup(Resource):
    """Handles api registration url api/auth/signup."""

    @auth_namespace.doc('create new user')
    @auth_namespace.expect(registration_model)
    def post(self):
        """create a new user to database"""
        data = request.get_json()
        first_name = data['FirstName']
        last_name = data['LastName']
        email = data['Email']
        password = data['Password']

        user = User(first_name, last_name, email, password)
        user.create()

        return {
            'status': 'success',
            'message': 'Successfully registered.'
        }, 201
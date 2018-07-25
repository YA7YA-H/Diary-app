from flask_restplus import Resource, Namespace, fields
from flask import request
from flask_bcrypt import Bcrypt
from Api_v1.app.models.user import user_data, User
from Api_v1.app.models.token import token_required
from Api_v1.Database.connector import DatabaseConnection
from Api_v1.app.models.blacklist import Blacklist, blacklist
import re
database = DatabaseConnection()
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

login_model = auth_namespace.model(
    'Login', {
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

email_expression = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pattern = re.compile(r"(^[A-Za-z]+$)")


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
        query_email = database.getall_email()

        confirm = bool([
            existing_email for existing_email in query_email
            if " ".join(list(existing_email)) == email
        ])
        print(query_email)
        if confirm:
            return {"Message": "Email already exist"}, 401
        try:
            if (len(first_name) or len(last_name)) < 2:
                return {
                    "Status": "Error",
                    "Message": "Names should be more than 2 "
                }, 400
            if not (re.match(pattern, first_name)
                    and re.match(pattern, last_name)):
                return {
                    "Status": "Error",
                    "Message": "Invalid character in your name(s)"
                }, 400
            if len(password) < 6:
                return {
                    "Status": "Error",
                    "Message": "Password should be more than 6 character "
                }, 400
            if len(email) < 4:
                return {
                    "Status": "Error",
                    "Message": "Email should be more than 4 character "
                }, 400
            if not re.match(email_expression, email):
                return {
                    "Status": "Error",
                    "Message": "Invalid character in your email "
                }, 400

        except (KeyError) as e:
            return {"Message": str(e)}
        else:
            user = User(first_name, last_name, email, password)
            user.create()
            return {
                'status': 'success',
                'message': 'Successfully registered.'
            }, 201


# @auth_namespace.route('/login')
# @auth_namespace.doc(
#     responses={
#         201: 'Successfully login',
#         401: 'Invalid credential'
#     },
#     security=None,
#     body=login_model)
# class Login(Resource):
#     """Handles api registration url api/auth/signin."""

#     def post(self):
#         """Handle POST request for login"""
#         post_data = request.get_json()
#         user_email = post_data['Email']
#         user_password = post_data['Password']

#         if user_email in user_data:
#             if Bcrypt().check_password_hash(user_data[user_email]["Password"],
#                                             user_password):
#                 # # generate the auth token
#                 auth_token = User.encode_auth_token(user_email)

#                 return {
#                     'status': 'success',
#                     'message': 'Successfully login.',
#                     'auth_token': auth_token.decode('UTF-8')
#                 }, 201
#             else:
#                 return {
#                     "message": "Failed, Invalid password! Please try again"
#                 }, 401
#         else:
#             return {"message": "Failed, Invalid email! Please try again"}, 401

# @auth_namespace.route('/logout')
# @auth_namespace.doc(
#     responses={
#         201: 'Successfully login',
#         401: 'Invalid credential'
#     },
#     security="apikey")
# class Logout(Resource):
#     """Handles logout Routes"""

#     @token_required
#     def post(self, current_user):
#         """Handle POST request for logout"""

#         # get auth token
#         token = request.headers['access_token']

#         # mark the token as blacklisted
#         try:
#             revokedToken = Blacklist(token)
#             revokedToken.save_blacklist()

#         except Exception as e:
#             return {'status': 'Failed to logout', 'message': str(e)}, 200

#         else:
#             return {
#                 'status': 'success',
#                 'message': 'Successfully logged out.'
#             }, 200

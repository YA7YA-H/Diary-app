from flask import Flask
from flask_restplus import Api
from Api_v1.configurations.config import app_config
from Api_v1.Database.connector import DatabaseConnection

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'access_token'
    }
}

api = Api(
    version="1.0",
    authorizations=authorization,
    title="MY DIARY API",
    description="A simple My Diary API",
    prefix='/api/v1')

#delete default namespace
del api.namespaces[0]
db = DatabaseConnection()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # from Api_v1.endpoints.contents import entries_namespace as entries
    from Api_v1.endpoints.auth import auth_namespace as auth
    # api.add_namespace(entries, path='/user')
    api.add_namespace(auth, path='/auth')
    api.init_app(app)
    return app
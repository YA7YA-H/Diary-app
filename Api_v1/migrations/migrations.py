import os

from Api_v1.Database.connector import DatabaseConnection

db = DatabaseConnection(os.environ['APP_SETTINGS'])


def setup():
    try:
        db.create_tables_user()
        db.create_tables_entry()
    except:
        print('DATABASE TABLE ALREADY EXIST')
        pass


setup()
import unittest

from flask import current_app
from Api_v1.app.app import create_app


class TestDevelopmentConfig(unittest.TestCase):
    def test_app_is_development(self):
        app = create_app("development")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['DATABASE_URI'] ==
                        "postgresql://postgres:hassan@localhost/mydiarydb")


class TestTestingConfig(unittest.TestCase):
    def test_app_is_testing(self):
        app = create_app("testing")
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['DATABASE_URI'] ==
                        "postgresql://postgres:hassan@localhost/testdb")


class TestProductionConfig(unittest.TestCase):
    def test_app_is_production(self):
        app = create_app("production")
        self.assertTrue(app.config['DEBUG'] is False)
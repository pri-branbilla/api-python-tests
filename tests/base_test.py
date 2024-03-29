from unittest import TestCase
from db import db
from app import app


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI  # noqa: E501
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

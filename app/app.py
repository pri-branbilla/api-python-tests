import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from app.security import authenticate, identity
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList
from app.resources.user import UserRegister

appl = Flask(__name__)

appl.config['DEBUG'] = True

appl.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
                                                        'DATABASE_URL',
                                                        'sqlite:///data.db'
                                                        )
appl.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
appl.config['PROPAGATE_EXCEPTIONS'] = True
appl.secret_key = 'test'
api = Api(appl)

jwt = JWT(appl, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


@appl.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({
        'message': 'Unauthorized.'
    }), 401


if __name__ == '__main__':
    from app.db import db

    db.init_app(appl)

    if appl.config['DEBUG']:
        @appl.before_first_request
        def create_tables():
            db.create_all()

    appl.run(port=5000)

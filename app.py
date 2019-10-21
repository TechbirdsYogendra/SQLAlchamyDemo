from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity as identity_function

from resources.user import UserRegister, Users
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = "yogendra"
api = Api(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
jwt = JWT(app, authenticate, identity_function)  # creates a end point /auth

# Create database and all the tables.
@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    # This below line will execute only if we run this file not in the case of import.
    from db import db

    db.init_app(app)
    app.run(port=500, debug=True)

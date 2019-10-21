import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="username is required to register")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="password is required to register")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is None:
            # user = UserModel(data["username"], data["password"])
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "User is created successfully."}
        else:
            return {"message": "User is already exits with this username choose another username."}, 400


class Users(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM users"
        users = cursor.execute(select_query).fetchall()

        connection.commit()
        connection.close()

        return {"users": users}

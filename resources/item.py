from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Please pass price as well"
                        )

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Store id is required"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 400

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"The item with name {name} is already exist."}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500  # Internal Server Error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item Deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data["price"], data["store_id"]) # or
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
        # return {"items": [item.json() for item in ItemModel.query.all()]}

from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "No store is found with this name"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store with {name} is already exist"}

        try:
            store = StoreModel(name)
            store.save_to_db()
        except:
            return {"error": "Error occurred while creating the store"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store is deleted"}


class StoreList(Resource):

    def get(self):
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}

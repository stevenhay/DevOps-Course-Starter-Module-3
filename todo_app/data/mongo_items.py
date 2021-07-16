from datetime import datetime
import os

from bson.objectid import ObjectId
from todo_app.data.todo_item import Item
import pymongo

class MongoDB:
    collection_names = ['To Do', 'Doing', 'Done']

    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.brtrv.mongodb.net/{os.getenv('MONGO_DATABASE')}?w=majority")
        self.db = self.client.get_default_database()

    def get_collection(self, name):
        """
        Fetches the collection from the MongoDB with the specified name.

        Args:
            name (str): The name of the list.

        Returns:
            collection: The collection, or None if no collection matches the specified name.
        """
        return self.db.get_collection(name)


    def get_items(self):
        """
        Fetches all items from Mongo

        Returns:
            list: The list of saved items.
        """
        items = []
        for cname in self.collection_names:
            for item in self.get_collection(cname).find():
                items.append(Item.fromMongo(item, cname))

        return items


    def get_item(self, id):
        """
        Fetches the item with the specified ID.

        Args:
            id (str): The ID of the item.

        Returns:
            item: The item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item['id'] == id), None)


    def add_item(self, name):
        """
        Adds a new item with the specified name.

        Args:
            name (str): The name of the item.

        Returns:
            item: The saved item.
        """
        item = {
            'name': name,
            'dateLastActivity': str(datetime.utcnow())
        }
        inserted_id = self.db.get_collection('To Do').insert_one(item).inserted_id
        return Item(inserted_id, item['name'], item['dateLastActivity'])


    def start_item(self, id):
        """
        Moves the item with the specified ID to the "Doing" collection.

        Args:
            id (str): The ID of the item.
        """
        self.move(id, 'To Do', 'Doing')


    def complete_item(self, id):
        """
        Moves the item with the specified ID to the "Done" collection.

        Args:
            id (str): The ID of the item.
        """
        self.move(id, 'Doing', 'Done')


    def uncomplete_item(self, id):
        """
        Moves the item with the specified ID to the "To-Do" collection.

        Args:
            id (str): The ID of the item.
        """
        self.move(id, 'Done', 'To Do')


    def move(self, id, src, dst):
        item = self.db.get_collection(src).find_one_and_delete({"_id":  ObjectId(id)})
        item['dateLastActivity'] = datetime.utcnow()
        self.db.get_collection(dst).insert_one(item)

from datetime import datetime

class Item:

    def __init__(self, id, name, last_modified, status = 'To Do'):
        self.id = id
        self.name = name
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def fromMongo(cls, item, status):
        return cls(item['_id'], item['name'], item['dateLastActivity'], status)

    @property
    def last_modified_today(self):
        return self.last_modified.date() == datetime.now().date()

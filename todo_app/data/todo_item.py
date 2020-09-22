from dateutil.parser import isoparse
from datetime import datetime

class Item:

    def __init__(self, id, name, last_modified, status = 'To Do'):
        self.id = id
        self.name = name
        self.last_modified = isoparse(last_modified)
        self.status = status

    @classmethod
    def fromTrelloCard(cls, card, list):
        return cls(card['id'], card['name'], card['dateLastActivity'], list['name'])

    @property
    def last_modified_today(self):
        return self.last_modified.date() == datetime.now().date()

    def reset(self):
        self.status = 'To Do'

    def start(self):
        self.status = 'Doing'

    def complete(self):
        self.status = 'Done'

from todo_app.data.mongo_items import MongoDB
from todo_app.data.todo_item import Item
from todo_app.app import create_app
from dotenv import find_dotenv, load_dotenv
from dateutil.parser import isoparse
import pytest
import pymongo

def data(self):
    return [
            Item("1", "Card 1", isoparse("2020-09-12T22:01:24.072Z"), "To Do"),
            Item("2", "Card 2", isoparse("2020-09-12T22:01:24.072Z"), "To Do"),
            Item("3", "Card 3", isoparse("2020-09-12T22:01:24.072Z"), "Doing"),
            Item("4", "Card 4", isoparse("2020-09-12T22:01:24.072Z"), "Doing"),
    ]

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()
    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(pymongo, 'MongoClient', lambda _: None)
    monkeypatch.setattr(MongoDB, 'get_items', data)

    response = client.get('/')
    print (response)

    assert b'<h5 class="mb-1">Card 1</h5>' in response.data
    assert b'<h5 class="mb-1">Card 2</h5>' in response.data
    assert b'<h5 class="mb-1">Card 3</h5>' in response.data
    assert b'<h5 class="mb-1">Card 4</h5>' in response.data

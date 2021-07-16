from todo_app.model.view_model import ViewModel
from todo_app.data.todo_item import Item
from dateutil.parser import isoparse
from unittest.mock import patch
import pytest
import datetime

class MockDate(datetime.date):
    @classmethod
    def now(cls):
        return isoparse('2020-08-24T20:45:04.888Z')


def mkitem(status, id='id', name='name', last_modified='2020-08-24T20:45:04.888Z'):
    return Item(id, name, isoparse(last_modified), status)

model = ViewModel([
    mkitem(status='To Do'),
    mkitem(status='To Do'), 
    mkitem(status='Doing'), 
    mkitem(status='Doing'), 
    mkitem(status='Done'), 
    mkitem(status='Done')
])

def test_items_property():
    assert len(model.items) == 6

def test_todo_items_property():
    for item in model.todo_items:
        if item.status != 'To Do':
            pytest.fail('An item returned by todo_items was not in the To Do state!')

    assert len(model.todo_items) == 2

def test_doing_items_property():
    for item in model.doing_items:
        if item.status != 'Doing':
            pytest.fail('An item returned by todo_items was not in the Doing state!')

    assert len(model.todo_items) == 2

def test_done_items_property():
    for item in model.done_items:
        if item.status != 'Done':
            pytest.fail('An item returned by todo_items was not in the Done state!')

    assert len(model.todo_items) == 2

def test_show_all_done_items_property():
    model = ViewModel([mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done')])
    assert model.show_all_done_items == False

    model = ViewModel([mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done')])
    assert model.show_all_done_items == False

    model = ViewModel([mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done'), mkitem(status='Done')])
    assert model.show_all_done_items == True

@patch('todo_app.data.todo_item.datetime', MockDate)
def test_recent_done_items():
    model = ViewModel([mkitem(status='Done', last_modified='2020-08-24T20:45:04.888Z')])
    assert len(model.recent_done_items) == 1

    model = ViewModel([mkitem(status='Done', last_modified='2020-08-24T20:45:04.888Z'), mkitem(status='Done', last_modified='2020-06-24T20:45:04.888Z')])
    assert len(model.recent_done_items) == 1

    model = ViewModel([mkitem(status='To Do', last_modified='2020-08-24T20:45:04.888Z')])
    assert len(model.recent_done_items) == 0

    model = ViewModel([mkitem(status='Done', last_modified='2020-06-24T20:45:04.888Z')])
    assert len(model.recent_done_items) == 0

@patch('todo_app.data.todo_item.datetime', MockDate)
def test_older_done_items():
    model = ViewModel([mkitem(status='Done', last_modified='2020-06-24T20:45:04.888Z')])
    assert len(model.older_done_items) == 1

    model = ViewModel([mkitem(status='Done', last_modified='2020-06-24T20:45:04.888Z'), mkitem(status='Done', last_modified='2020-08-24T20:45:04.888Z')])
    assert len(model.older_done_items) == 1

    model = ViewModel([mkitem(status='To Do', last_modified='2020-06-24T20:45:04.888Z')])
    assert len(model.older_done_items) == 0

    model = ViewModel([mkitem(status='Done', last_modified='2020-08-24T20:45:04.888Z')])
    assert len(model.older_done_items) == 0

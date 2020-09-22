from todo_app.app import create_app
from dotenv import find_dotenv, load_dotenv
import pytest
import requests

class MockBoardsResponse:
    @staticmethod
    def json():
        return  [
            {
                "name": "Test Board",
                "id": "12345",
                "url": "http://localhost/"
            }
        ]

class MockListsResponse:
    @staticmethod
    def json():
        return [
            {
                "name": "To Do",
                "cards": [
                    {
                        "id": "1",
                        "dateLastActivity": "2020-09-12T22:01:24.072Z",
                        "name": "Card1"
                    },
                    {
                        "id": "2",
                        "dateLastActivity": "2020-09-12T22:01:24.072Z",
                        "name": "Card2"
                    }
                ]
            },
            {
                "name": "Done",
                "cards": [
                    {
                        "id": "3",
                        "dateLastActivity": "2020-09-12T22:01:24.072Z",
                        "name": "Card3"
                    },
                    {
                        "id": "4",
                        "dateLastActivity": "2020-09-12T22:01:24.072Z",
                        "name": "Card4"
                    }
                ]
            }
        ]

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def mock_get_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        url = args[0]
        if url.endswith("/boards"):
           return MockBoardsResponse()
        elif url.endswith("/lists"):
            return MockListsResponse()

        raise RuntimeError("Requested url not mocked")
    
    monkeypatch.setattr(requests, "get", mock_get)

def test_index_page(mock_get_requests, client):
    response = client.get('/')
    print (response)

    assert b'<h5 class="mb-1">Card1</h5>' in response.data
    assert b'<h5 class="mb-1">Card2</h5>' in response.data
    assert b'<h5 class="mb-1">Card3</h5>' in response.data
    assert b'<h5 class="mb-1">Card4</h5>' in response.data

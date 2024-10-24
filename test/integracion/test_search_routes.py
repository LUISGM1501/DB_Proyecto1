from flask_jwt_extended import create_access_token
from unittest.mock import patch
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.search_controller.search_content')
def test_search(mock_search_content, client):
    mock_search_content.return_value = [
        {
            "id": 1,
            "content_type": "post",
            "title": "Test Post",
            "description": "This is a test post.",
            "created_at": "2023-10-01"
        },
        {
            "id": 2,
            "content_type": "place",
            "title": "Test Place",
            "description": "This is a test place.",
            "created_at": "2023-10-02"
        }
    ]

    access_token = create_access_token(identity=1)

    response = client.get(
        '/search',
        headers={'Authorization': f'Bearer {access_token}'},
        query_string={'q': 'test'}
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "content_type": "post",
            "title": "Test Post",
            "description": "This is a test post.",
            "created_at": "2023-10-01"
        },
        {
            "id": 2,
            "content_type": "place",
            "title": "Test Place",
            "description": "This is a test place.",
            "created_at": "2023-10-02"
        }
    ]

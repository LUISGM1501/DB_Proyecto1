# test/integracion/test_like_routes.py

import pytest
from flask_jwt_extended import create_access_token
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.like_controller.add_like')
def test_add_like_success(mock_add_like, client):
    mock_add_like.return_value = True

    access_token = create_access_token(identity=1)

    response = client.post(
        '/likes',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'user_id': 1,
            'post_id': 123
        }
    )

    assert response.status_code == 201
    assert response.get_json() == {"message": "Like added successfully"}

@patch('controllers.like_controller.add_like')
def test_add_like_already_exists(mock_add_like, client):
    mock_add_like.return_value = False

    access_token = create_access_token(identity=1)

    response = client.post(
        '/likes',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'user_id': 1,
            'post_id': 123
        }
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Like already exists"}

@patch('controllers.like_controller.get_like_count')
def test_get_like_count(mock_get_like_count, client):
    mock_get_like_count.return_value = 10

    access_token = create_access_token(identity=1)

    response = client.get(
        '/likes/count',
        headers={'Authorization': f'Bearer {access_token}'},
        query_string={'post_id': 123}
    )

    assert response.status_code == 200
    assert response.get_json() == {"count": 10}

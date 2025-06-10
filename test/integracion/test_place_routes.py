from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.place_controller.create_place')
def test_create_place(mock_create_place, client):
    mock_create_place.return_value = 1
    with app.app_context():
        access_token = create_access_token(identity="1")
    response = client.post(
        '/places',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'name': 'Test Place',
            'description': 'A place for testing',
            'city': 'Test City',
            'country': 'Test Country'
        }
    )

    assert response.status_code == 201
    assert response.get_json() == {"message": "Place created successfully", "place_id": 1}

@patch('controllers.place_controller.get_place')
def test_get_place(mock_get_place, client):
    mock_get_place.return_value = {
        'id': 1,
        'name': 'Test Place',
        'description': 'A place for testing',
        'city': 'Test City',
        'country': 'Test Country'
    }
    with app.app_context():
        access_token = create_access_token(identity="1")
    response = client.get(
        '/places/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.get_json() == mock_get_place.return_value

@patch('controllers.place_controller.update_place')
def test_update_place(mock_update_place, client):
    mock_update_place.return_value = 1
    with app.app_context():
        access_token = create_access_token(identity="1")
    response = client.put(
        '/places/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'name': 'Updated Place',
            'description': 'Updated description',
            'city': 'Updated City',
            'country': 'Updated Country'
        }
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Place updated successfully", "place_id": 1}

@patch('controllers.place_controller.delete_place')
def test_delete_place(mock_delete_place, client):
    mock_delete_place.return_value = 1
    with app.app_context():
        access_token = create_access_token(identity="1")
    response = client.delete(
        '/places/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Place deleted successfully", "place_id": 1}

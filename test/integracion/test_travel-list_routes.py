from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app
from models import travel_list

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.travel_list_controller.create_travel_list')
def test_create_travel_list(mock_create_travel_list, client):
    mock_create_travel_list.return_value = 1
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.post(
        '/travel-lists',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'user_id': 1, 'name': 'My Travel List', 'description': 'A description'}
    )

    assert response.status_code == 201  # CORRECTO
    assert response.json == {"message": "Travel list created successfully", "list_id": 1}


@patch('controllers.travel_list_controller.get_travel_list')
def test_get_travel_list(mock_get_travel_list, client):
    mock_get_travel_list.return_value = travel_list.TravelList(1, 'My Travel List', 'A description')    
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.get(
        '/travel-lists/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    

    expected_response = {
        "id": None,
        "user_id": 1,
        "name": "My Travel List",
        "description": "A description"
    }
    
    assert response.status_code == 200
    assert all(item in response.json.items() for item in expected_response.items())
    
@patch('controllers.travel_list_controller.update_travel_list')
@patch('controllers.travel_list_controller.get_travel_list')
def test_update_travel_list(mock_get_travel_list, mock_update_travel_list, client):
    mock_get_travel_list.return_value = travel_list.TravelList("1", 'Old Name', 'Old Description')  # STRING
    mock_update_travel_list.return_value = 1 
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.put(
        '/travel-lists/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'name': 'Updated Name', 'description': 'Updated Description'}
    )

    assert response.status_code == 200  # CORRECTO
    assert response.json == {"message": "Travel list updated successfully", "list_id": 1}

@patch('controllers.travel_list_controller.delete_travel_list')
@patch('controllers.travel_list_controller.get_travel_list')
def test_delete_travel_list(mock_get_travel_list, mock_delete_travel_list, client):
    mock_get_travel_list.return_value = travel_list.TravelList("1", 'My Travel List', 'A description')  # STRING
    mock_delete_travel_list.return_value = 1
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.delete(
        '/travel-lists/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200  # CORRECTO
    assert response.json == {"message": "Travel list deleted successfully", "list_id": 1}
    
@patch('controllers.travel_list_controller.add_place_to_list')
@patch('controllers.travel_list_controller.get_travel_list')
def test_add_place_to_list(mock_get_travel_list, mock_add_place_to_list, client):
    mock_get_travel_list.return_value = travel_list.TravelList("1", 'My Travel List', 'A description')  # STRING
    mock_add_place_to_list.return_value = 1  # ID simulado de entrada de lugar
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.post(
        '/travel-lists/1/places',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'place_id': 1}
    )

    assert response.status_code == 201  # CORRECTO
    assert response.json == {"message": "Place added to travel list successfully", "entry_id": 1}

@patch('controllers.travel_list_controller.remove_place_from_list')
@patch('controllers.travel_list_controller.get_travel_list')
def test_remove_place_from_list(mock_get_travel_list, mock_remove_place_from_list, client):
    mock_get_travel_list.return_value = travel_list.TravelList("1", 'My Travel List', 'A description')  # STRING
    mock_remove_place_from_list.return_value = 1
    
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    response = client.delete(
        '/travel-lists/1/places/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200  # CORRECTO
    assert response.json == {"message": "Place removed from travel list successfully", "entry_id": 1}

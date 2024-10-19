from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app
from models import user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_create_user(client, mocker):
    mock_create_user = mocker.patch('controllers.user_controller.create_user')
    mock_create_user.return_value = 1
    
    access_token = create_access_token(identity=1)
    response = client.post(
        '/users',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'bio': 'Test bio',
            'profile_picture_url': 'http://example.com/profile.jpg'
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 201
    assert response.json == {"message": "User created successfully", "user_id": 1}

# Prueba de obtención de usuario por ID
def test_get_user(client, mocker):
    mock_get_user = mocker.patch('controllers.user_controller.get_user')
    mock_get_user.return_value = user.User(
        id=1,
        username='testuser',
        email='testuser@example.com',
        password='password',
        bio='Test bio',
        profile_picture_url='http://example.com/profile.jpg'
    )

    access_token = create_access_token(identity=1)
    response = client.get(
        '/users/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    expected_response = {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "bio": "Test bio",
        "profile_picture_url": "http://example.com/profile.jpg"
    }

    assert response.status_code == 200
    assert all(item in response.json.items() for item in expected_response.items())

# @patch('services.auth_service.authenticate_user')
# def test_login(mock_authenticate_user, client):
#     mock_authenticate_user.return_value = create_access_token(identity=1)  # Simula un token de acceso
    
#     response = client.post(
#         '/login',
#         json={'username': 'testuser', 'password': 'testpassword'}
#     )

#     assert response.status_code == 200, f"Unexpected error: {response.json}"
#     assert 'access_token' in response.json


# Prueba de ruta protegida
def test_protected_route(client):
    access_token = create_access_token(identity=1)
    response = client.get(
        '/protected',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json == {'logged_in_as': 1}

# Prueba de refresh token
def test_refresh_token(client):
    refresh_token = create_access_token(identity=1, additional_claims={"type": "refresh"})
    
    response = client.post(
        '/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    assert response.status_code == 200, f"Unexpected error: {response.json}"
    assert 'access_token' in response.json

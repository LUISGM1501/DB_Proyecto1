from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app
from models import user

# Usar fixture común de conftest.py
# @pytest.fixture definido en conftest.py

def test_create_user(client, mocker):
    """Test para crear usuario"""
    mock_create_user = mocker.patch('controllers.user_controller.create_user')
    mock_create_user.return_value = 1
    
    # Crear token correctamente con string
    with app.app_context():
        access_token = create_access_token(identity="1")  # STRING, no integer
    
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

def test_get_user(client, mocker):
    """Test para obtener usuario"""
    mock_get_user = mocker.patch('controllers.user_controller.get_user')
    mock_get_user.return_value = user.User(
        id=1,
        username='testuser',
        email='testuser@example.com',
        password='password',
        bio='Test bio',
        profile_picture_url='http://example.com/profile.jpg'
    )

    # Crear token correctamente
    with app.app_context():
        access_token = create_access_token(identity="1")

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

def test_protected_route(client):
    """Test de ruta protegida"""
    with app.app_context():
        access_token = create_access_token(identity="1")  # STRING
    
    response = client.get(
        '/protected',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json == {'logged_in_as': "1"}  # Comparar con string

def test_refresh_token(client):
    """Test de refresh token"""
    with app.app_context():
        # Crear refresh token correctamente
        refresh_token = create_access_token(
            identity="1",  # STRING
            additional_claims={"type": "refresh"}
        )
    
    response = client.post(
        '/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    assert response.status_code == 200
    assert 'access_token' in response.json

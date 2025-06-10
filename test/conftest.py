# tests/conftest.py
import pytest
from flask_jwt_extended import create_access_token
from app import app

@pytest.fixture
def client():
    """Cliente de pruebas común para todas las pruebas de integración"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def auth_headers():
    """Headers de autenticación con token válido"""
    with app.app_context():
        # IMPORTANTE: El identity debe ser STRING, no integer
        access_token = create_access_token(identity="1")
        return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture
def auth_token():
    """Token de autenticación válido"""
    with app.app_context():
        return create_access_token(identity="1")
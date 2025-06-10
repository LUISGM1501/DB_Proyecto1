from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app
from config import database as connections

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_postgres_connection(client):
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    connection = connections.get_postgres_connection()
    assert connection is not None, "La conexión a PostgreSQL falló"

    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    
    assert result[0] == 1, "La conexión a PostgreSQL no es válida"
    
    cursor.close()
    connection.close()

def test_mongo_connection(client):
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    db = connections.get_mongo_connection()    
    assert db is not None, "La conexión a MongoDB falló"

    result = db.test_collection.find_one({"test": "value"})
    assert result is None or isinstance(result, dict), "La conexión a MongoDB no es válida"

def test_redis_connection(client):
    with app.app_context():
        access_token = create_access_token(identity="1")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    redis_client = connections.get_redis_connection()
    
    assert redis_client is not None, "La conexión a Redis falló"

    redis_client.set('test_key', 'test_value')
    result = redis_client.get('test_key')    
    assert result == 'test_value', "La conexión a Redis no es válida"
    
    redis_client.delete('test_key')

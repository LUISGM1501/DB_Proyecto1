import pytest
from config import database as connections

def test_postgres_connection():
    connection = connections.get_postgres_connection()
    assert connection is not None, "La conexión a PostgreSQL falló"

    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    
    assert result[0] == 1, "La conexión a PostgreSQL no es válida"
    
    cursor.close()
    connection.close()

def test_mongo_connection():
    db = connections.get_mongo_connection()    
    assert db is not None, "La conexión a MongoDB falló"

    result = db.test_collection.find_one({"test": "value"})
    assert result is None or isinstance(result, dict), "La conexión a MongoDB no es válida"

def test_redis_connection():
    redis_client = connections.get_redis_connection()
    
    assert redis_client is not None, "La conexión a Redis falló"

    redis_client.set('test_key', 'test_value')
    result = redis_client.get('test_key')    
    assert result == 'test_value', "La conexión a Redis no es válida"
    
    redis_client.delete('test_key')

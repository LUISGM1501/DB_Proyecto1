import os
import sys
import pytest
import mongomock
import fakeredis

# Agregar el directorio raíz al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

@pytest.fixture(autouse=True)
def mock_mongodb(monkeypatch):
    mock_mongo = mongomock.MongoClient()
    def mock_get_mongo_connection():
        return mock_mongo.db
    monkeypatch.setattr('config.database.get_mongo_connection', mock_get_mongo_connection)
    return mock_mongo

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_redis_client = fakeredis.FakeRedis()
    def mock_get_redis_connection():
        return fake_redis_client
    monkeypatch.setattr('config.database.get_redis_connection', mock_get_redis_connection)
    return fake_redis_client

@pytest.fixture
def app():
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()
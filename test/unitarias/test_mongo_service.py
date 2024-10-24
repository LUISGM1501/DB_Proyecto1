# tests/unit/test_mongo_service.py
import pytest
from datetime import datetime
from src.services.mongo_service import MongoService
from bson import ObjectId

@pytest.fixture
def mongo_service():
    return MongoService()

def test_create_travel_details(mongo_service, mocker):
    # Mock de la conexión a MongoDB
    mock_insert = mocker.patch.object(mongo_service.db.travel_details, 'insert_one')
    mock_insert.return_value.inserted_id = ObjectId('507f1f77bcf86cd799439011')
    
    travel_data = {
        'title': 'Test Travel',
        'description': 'Test Description',
        'places': []
    }
    
    result = mongo_service.create_travel_details(travel_data)
    
    assert isinstance(result, str)
    assert len(result) == 24  # ObjectId length
    mock_insert.assert_called_once()

def test_create_user_stats(mongo_service, mocker):
    mock_insert = mocker.patch.object(mongo_service.db.user_stats, 'insert_one')
    mock_insert.return_value.inserted_id = ObjectId('507f1f77bcf86cd799439011')
    
    result = mongo_service.create_user_stats(user_id=1)
    
    assert isinstance(result, str)
    mock_insert.assert_called_once()
    
def test_update_user_stats(mongo_service, mocker):
    mock_update = mocker.patch.object(mongo_service.db.user_stats, 'update_one')
    mock_update.return_value.modified_count = 1
    
    update_data = {'total_posts': 5}
    result = mongo_service.update_user_stats(user_id=1, update_data=update_data)
    
    assert result is True
    mock_update.assert_called_once()

def test_create_activity_log(mongo_service, mocker):
    mock_insert = mocker.patch.object(mongo_service.db.activity_logs, 'insert_one')
    mock_insert.return_value.inserted_id = ObjectId('507f1f77bcf86cd799439011')
    
    result = mongo_service.create_activity_log(
        user_id=1,
        activity_type='test',
        details={'test': 'data'}
    )
    
    assert isinstance(result, str)
    mock_insert.assert_called_once()

def test_get_user_activity_logs(mongo_service, mocker):
    mock_find = mocker.patch.object(mongo_service.db.activity_logs, 'find')
    mock_find.return_value.sort.return_value.limit.return_value = [
        {'activity_type': 'test1'},
        {'activity_type': 'test2'}
    ]
    
    results = mongo_service.get_user_activity_logs(user_id=1, limit=2)
    
    assert len(results) == 2
    mock_find.assert_called_once_with({'user_id': 1})
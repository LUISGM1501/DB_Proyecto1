# tests/unit/test_redis_service.py
import pytest
from src.services.redis_service import RedisService
from datetime import datetime, UTC
import json

@pytest.fixture
def redis_service():
    return RedisService()

def test_cache_post(redis_service, mocker):
    mock_redis = mocker.patch.object(redis_service, 'redis_client')
    post_data = {'id': 1, 'content': 'Test post'}
    
    redis_service.cache_post(1, post_data)
    
    mock_redis.setex.assert_called_once_with(
        f'post:{1}',
        redis_service.default_expire,
        json.dumps(post_data)
    )

def test_get_cached_post(redis_service, mocker):
    mock_redis = mocker.patch.object(redis_service, 'redis_client')
    post_data = {'id': 1, 'content': 'Test post'}
    mock_redis.get.return_value = json.dumps(post_data)
    
    result = redis_service.get_cached_post(1)
    
    assert result == post_data
    mock_redis.get.assert_called_once_with(f'post:{1}')

def test_create_user_session(redis_service, mocker):
    mock_redis = mocker.patch.object(redis_service, 'redis_client')
    session_data = {
        'user_id': 1,
        'username': 'test_user',
        'created_at': datetime.now(UTC).isoformat()
    }
    
    redis_service.create_user_session(1, session_data)
    
    mock_redis.setex.assert_called_once()
    # Verificamos que el argumento sea serializable
    json.dumps(mock_redis.setex.call_args[0][2])

def test_check_rate_limit(redis_service, mocker):
    mock_redis = mocker.patch.object(redis_service, 'redis_client')
    mock_redis.get.return_value = '5'
    
    result = redis_service.check_rate_limit(1, 'test_action', 10)
    
    assert result is True
    mock_redis.incr.assert_called_once()
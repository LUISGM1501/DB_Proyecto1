import pytest
from src.services.cache_service import cache_post, get_cached_post, cache_popular_posts, get_cached_popular_posts

def test_cache_post(mocker):
    mock_redis = mocker.patch('services.cache_service.redis_client')
    
    post_id = 1
    post_data = {"title": "Test Post", "content": "This is a test"}
    
    cache_post(post_id, post_data)
    
    mock_redis.setex.assert_called_once_with(f"post:{post_id}", 3600, str(post_data))

def test_get_cached_post(mocker):
    mock_redis = mocker.patch('services.cache_service.redis_client')
    
    post_id = 1
    post_data = {"title": "Test Post", "content": "This is a test"}
    
    mock_redis.get.return_value = str(post_data)
    
    cached_post = get_cached_post(post_id)
    
    mock_redis.get.assert_called_once_with(f"post:{post_id}")
    assert cached_post == post_data

def test_cache_popular_posts(mocker):
    mock_redis = mocker.patch('services.cache_service.redis_client')
    
    popular_posts = [{"title": "Popular Post 1"}, {"title": "Popular Post 2"}]
    
    cache_popular_posts(popular_posts)
    
    mock_redis.setex.assert_called_once_with("popular_posts", 3600, str(popular_posts))

def test_get_cached_popular_posts(mocker):
    mock_redis = mocker.patch('services.cache_service.redis_client')
    
    popular_posts = [{"title": "Popular Post 1"}, {"title": "Popular Post 2"}]
    
    mock_redis.get.return_value = str(popular_posts)
    
    cached_posts = get_cached_popular_posts()
    
    mock_redis.get.assert_called_once_with("popular_posts")
    assert cached_posts == popular_posts

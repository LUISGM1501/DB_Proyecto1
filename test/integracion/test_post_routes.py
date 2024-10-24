import pytest
from flask_jwt_extended import create_access_token
from src.app import app
from unittest.mock import patch
from src.models import post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.post_controller.create_post')
def test_create_post(mock_create_post, client):
    mock_create_post.return_value = 1
    access_token = create_access_token(identity=1)
    response = client.post(
        '/posts',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'user_id': 1, 'content': 'Test content'}
    )

    assert response.status_code == 201
    assert response.get_json() == {"message": "Post created successfully", "post_id": 1}

@patch('controllers.post_controller.get_post')
def test_get_post(mock_get_post, client):
    mock_get_post.return_value = {'id': 1, 'user_id': 1, 'content': 'Test content'}
    access_token = create_access_token(identity=1)
    response = client.get(
        '/posts/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'user_id': 1,
        'content': 'Test content'
    }

@patch('controllers.post_controller.get_posts_paginated')
def test_get_posts(mock_get_posts_paginated, client):
    mock_get_posts_paginated.return_value = ([{'id': 1, 'user_id': 1, 'content': 'Test content'}], 1)
    access_token = create_access_token(identity=1)
    response = client.get(
        '/posts',
        headers={'Authorization': f'Bearer {access_token}'},
        query_string={'page': 1, 'page_size': 10}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "posts": [{'id': 1, 'user_id': 1, 'content': 'Test content'}],
        "total_count": 1,
        "page": 1,
        "page_size": 10
    }

@patch('controllers.post_controller.get_post')
@patch('controllers.post_controller.update_post')
def test_update_post(mock_update_post, mock_get_post, client):
    mock_get_post.return_value = post.Post(id=1, user_id=1, content="Old content")
    mock_update_post.return_value = 1

    access_token = create_access_token(identity=1)

    response = client.put(
        '/posts/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'content': "Updated content"}
    )
    
    assert response.status_code == 200
    assert response.json["message"] == "Post updated successfully"
    
@patch('controllers.post_controller.get_post')
@patch('controllers.post_controller.delete_post')
def test_delete_post(mock_delete_post, mock_get_post, client):
    mock_get_post.return_value = post.Post(id=1, user_id=1, content="To be deleted")
    mock_delete_post.return_value = 1
    access_token = create_access_token(identity=1)

    response = client.delete(
        '/posts/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    assert response.status_code == 200
    assert response.json["message"] == "Post deleted successfully"

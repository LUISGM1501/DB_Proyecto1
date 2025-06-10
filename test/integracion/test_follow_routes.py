from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app
from unittest.mock import Mock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.follow_controller.follow_user')
def test_follow_user(mock_follow_user, client):
    mock_follow_user.return_value = 1 

    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.post(
        '/follow/2',  
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 201
    assert response.json == {"message": "User followed successfully", "follow_id": 1}
    mock_follow_user.assert_called_once_with("1", 2)  # Cambiado a string

@patch('controllers.follow_controller.unfollow_user')
def test_unfollow_user(mock_unfollow_user, client):
    mock_unfollow_user.return_value = 1  

    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.post(
        '/unfollow/2',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json == {"message": "User unfollowed successfully", "follow_id": 1}
    mock_unfollow_user.assert_called_once_with("1", 2)  # Cambiado a string

@patch('controllers.follow_controller.get_followed_users')
def test_get_followed_users(mock_get_followed_users, client):
    user_mock_1 = Mock()
    user_mock_1.to_dict.return_value = {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com"
    }

    user_mock_2 = Mock()
    user_mock_2.to_dict.return_value = {
        "id": 3,
        "username": "user3",
        "email": "user3@example.com"
    }

    mock_get_followed_users.return_value = [user_mock_1, user_mock_2]

    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.get(
        '/following',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200, f"Unexpected error: {response.get_json()}"
    assert len(response.json) == 2
    assert response.json[0]['username'] == 'user2'
    mock_get_followed_users.assert_called_once_with("1")  # Cambiado a string

@patch('controllers.follow_controller.get_followers')
def test_get_followers(mock_get_followers, client):
    user_mock_1 = Mock()
    user_mock_1.to_dict.return_value = {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com"
    }

    user_mock_2 = Mock()
    user_mock_2.to_dict.return_value = {
        "id": 4,
        "username": "user4",
        "email": "user4@example.com"
    }

    mock_get_followers.return_value = [user_mock_1, user_mock_2]

    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.get(
        '/followers',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200, f"Unexpected error: {response.get_json()}"
    assert len(response.json) == 2
    assert response.json[0]['username'] == 'user2'
    mock_get_followers.assert_called_once_with("1")  # Cambiado a string

@patch('controllers.follow_controller.get_feed')
def test_get_feed(mock_get_feed, client):
    
    mock_get_feed.return_value = [
        {"id": 1, "content": "Test post 1", "user_id": 2},
        {"id": 2, "content": "Test post 2", "user_id": 3}
    ]
    
    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.get(
        '/feed?page=1&page_size=10',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['content'] == 'Test post 1'
    mock_get_feed.assert_called_once_with("1", 1, 10)  # Cambiado a string

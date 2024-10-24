import pytest
from src.controllers import user_controller
from src.models.user import User

def test_create_user(mocker):
    mock_conn = mocker.patch('controllers.user_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    user_id = user_controller.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123",
        bio="Test user bio",
        profile_picture_url="http://example.com/profile.jpg"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_user(%s, %s, %s, %s, %s)", 
        ("testuser", "testuser@example.com", "password123", "Test user bio", "http://example.com/profile.jpg")
    )
    assert user_id == 1

def test_get_user(mocker):
    mock_conn = mocker.patch('controllers.user_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = ("testuser", "testuser@example.com", "password")
    user = user_controller.get_user(user_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_user_by_id(%s)", (1,)
    )
    
    print(user.id)
    print(user.username)
    print(user.email)
    print(user.bio)
    print(user.profile_picture_url)
    
    
    assert isinstance(user, User)
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.profile_picture_url == None
    assert user.bio == None

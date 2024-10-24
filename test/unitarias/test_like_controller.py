import pytest
from controllers import like_controller
from models.post import Post

def test_add_like_success(mocker):
    mock_conn = mocker.patch('controllers.like_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [True]

    mock_post = mocker.Mock()
    mock_post.user_id = 2
    
    mocker.patch('controllers.post_controller.get_post', return_value=mock_post)
    mock_create_notification = mocker.patch('controllers.notification_controller.create_notification')

    success = like_controller.add_like(user_id=1, post_id=123)

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_like(%s, %s, %s)",
        (1, 123, None)
    )
    mock_create_notification.assert_called_once_with(
        2, "comment", "User 1 commented on your post", 123
    )
    assert success is True

def test_add_like_no_notification(mocker):
    mock_conn = mocker.patch('controllers.like_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [True]
    
    mock_post = mocker.Mock()
    mock_post.user_id = 1 
    
    mocker.patch('controllers.post_controller.get_post', return_value=mock_post)
    mock_create_notification = mocker.patch('controllers.notification_controller.create_notification')

    success = like_controller.add_like(user_id=1, post_id=123)

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_like(%s, %s, %s)",
        (1, 123, None)
    )
    mock_create_notification.assert_not_called()

    assert success is True

def test_get_like_count(mocker):
    mock_conn = mocker.patch('controllers.like_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [10]

    like_count = like_controller.get_like_count(post_id=123)

    mock_cursor.execute.assert_called_once_with(
        "SELECT get_like_count(%s, %s)", (123, None)
    )
    assert like_count == 10

import pytest
from src.controllers import notification_controller

def test_create_notification(mocker):
    mock_conn = mocker.patch('controllers.notification_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    notification_id = notification_controller.create_notification(
        user_id=1,
        type="follow",
        content="User 2 followed you",
        related_id=None
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_notification(%s, %s, %s, %s)",
        (1, "follow", "User 2 followed you", None)
    )
    assert notification_id == 1

def test_get_user_notifications(mocker):
    mock_conn = mocker.patch('controllers.notification_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "comment", "User 2 commented on your post", 123, False, "2023-10-10"),
        (2, "like", "User 3 liked your post", 124, True, "2023-10-11")
    ]

    notifications = notification_controller.get_user_notifications(user_id=1, limit=10, offset=0)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_user_notifications(%s, %s, %s)", (1, 10, 0)
    )

    assert len(notifications) == 2
    assert notifications[0]["type"] == "comment"
    assert notifications[1]["type"] == "like"
    assert notifications[0]["is_read"] is False
    assert notifications[1]["is_read"] is True

def test_mark_notification_as_read(mocker):
    mock_conn = mocker.patch('controllers.notification_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [True]

    success = notification_controller.mark_notification_as_read(notification_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT mark_notification_as_read(%s)", (1,)
    )

    assert success is True
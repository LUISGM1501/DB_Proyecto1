# test/integracion/test_notification_routes.py

import pytest
from flask_jwt_extended import create_access_token
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.notification_controller.get_user_notifications')
def test_get_notifications(mock_get_user_notifications, client):
    mock_get_user_notifications.return_value = [
        {
            "id": 1,
            "type": "comment",
            "content": "User 1 commented on your post",
            "related_id": 123,
            "is_read": False,
            "created_at": "2023-10-13T10:00:00"
        },
        {
            "id": 2,
            "type": "follow",
            "content": "User 2 followed you",
            "related_id": None,
            "is_read": True,
            "created_at": "2023-10-13T11:00:00"
        }
    ]

    access_token = create_access_token(identity=1)

    response = client.get(
        '/notifications',
        headers={'Authorization': f'Bearer {access_token}'},
        query_string={'limit': 10, 'offset': 0}
    )

    assert response.status_code == 200
    assert response.get_json() == mock_get_user_notifications.return_value

@patch('controllers.notification_controller.mark_notification_as_read')
def test_mark_notification_read_success(mock_mark_notification_as_read, client):
    mock_mark_notification_as_read.return_value = True

    access_token = create_access_token(identity=1)

    response = client.post(
        '/notifications/1/read',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Notification marked as read"}

@patch('controllers.notification_controller.mark_notification_as_read')
def test_mark_notification_read_failure(mock_mark_notification_as_read, client):
    mock_mark_notification_as_read.return_value = False

    access_token = create_access_token(identity=1)

    response = client.post(
        '/notifications/1/read',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Failed to mark notification as read"}

# test/unitarias/test_follow_controller.py
import pytest
from controllers import follow_controller
from models.user import User
from models.post import Post

def test_follow_user_success(mocker):
    mock_conn = mocker.patch('controllers.follow_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    mock_create_notification = mocker.patch('controllers.notification_controller.create_notification')


    follow_id = follow_controller.follow_user(follower_id=1, followed_id=2)


    mock_cursor.execute.assert_called_once_with(
        "SELECT follow_user(%s, %s)", (1, 2)
    )
    mock_create_notification.assert_called_once_with(
        2, "follow", "User 1 followed you", None
    )

    assert follow_id == 1

def test_unfollow_user_success(mocker):
    mock_conn = mocker.patch('controllers.follow_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    unfollow_id = follow_controller.unfollow_user(follower_id=1, followed_id=2)

    mock_cursor.execute.assert_called_once_with(
        "SELECT unfollow_user(%s, %s)", (1, 2)
    )

    assert unfollow_id == 1

def test_get_followed_users(mocker):
    mock_conn = mocker.patch('controllers.follow_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('user1', 'user1@example.com', 'bio', 'profile_pic_url', '2023-10-10', '2023-10-10'),
        ('user2', 'user2@example.com', 'bio', 'profile_pic_url', '2023-10-10', '2023-10-10')
    ]

    followed_users = follow_controller.get_followed_users(user_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_followed_users(%s)", (1,)
    )

    assert len(followed_users) == 2
    assert isinstance(followed_users[0], User)
    assert followed_users[0].username == 'user1'

def test_get_followers(mocker):
    mock_conn = mocker.patch('controllers.follow_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
    ('user1', 'user1@example.com', 'bio', 'profile_pic_url', '2023-10-10', '2023-10-10'),
    ('user2', 'user2@example.com', 'bio', 'profile_pic_url', '2023-10-10', '2023-10-10')
    ]
    
    followers = follow_controller.get_followers(user_id=1)



    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_followers(%s)", (1,)
    )

    assert len(followers) == 2
    assert isinstance(followers[0], User)
    assert followers[0].username == 'user1'

def test_get_feed(mocker):
    mock_conn = mocker.patch('controllers.follow_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'First post', 'content1'),
        (2, 'Second post', 'content2')
    ]

    feed_posts = follow_controller.get_feed(user_id=1, page=1, page_size=10)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_feed(%s, %s, %s)", (1, 1, 10)
    )

    assert len(feed_posts) == 2
    assert isinstance(feed_posts[0], Post)
    assert feed_posts[0].content == 'First post'
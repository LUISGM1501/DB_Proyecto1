# tests/unit/test_comment_controller.py
import pytest
from controllers import comment_controller
from models.comment import Comment

def test_create_comment_success(mocker):
    # Mock de la conexión a la base de datos y la consulta
    mock_conn = mocker.patch('controllers.comment_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    # Simula el retorno de `cur.fetchone()` con un ID de comentario
    mock_cursor.fetchone.return_value = [1]

    # Mock de `post_controller.get_post` para verificar la notificación
    mock_post = mocker.Mock()
    mock_post.user_id = 2
    mocker.patch('controllers.post_controller.get_post', return_value=mock_post)

    # Mock de `notification_controller.create_notification` para evitar una notificación real
    mock_create_notification = mocker.patch('controllers.notification_controller.create_notification')

    # Ejecuta la función
    comment_id = comment_controller.create_comment(user_id=1, content="Test comment", post_id=123)

    # Verificaciones
    mock_cursor.execute.assert_called_once_with(
        "SELECT create_comment(%s, %s, %s, %s)",
        (1, "Test comment", 123, None)
    )
    mock_create_notification.assert_called_once_with(
        2, "comment", "User 1 commented on your post", 123
    )
    assert comment_id == 1

def test_create_comment_no_notification(mocker):
    # Mock de la conexión a la base de datos y la consulta
    mock_conn = mocker.patch('controllers.comment_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    # Simula el retorno de `cur.fetchone()` con un ID de comentario
    mock_cursor.fetchone.return_value = [2]

    # Mock de `post_controller.get_post` para simular que el usuario está comentando en su propio post
    mock_post = mocker.Mock()
    mock_post.user_id = 1  # Mismo user_id que el creador del comentario
    mocker.patch('controllers.post_controller.get_post', return_value=mock_post)

    # Mock de `notification_controller.create_notification` para evitar una notificación real
    mock_create_notification = mocker.patch('controllers.notification_controller.create_notification')

    # Ejecuta la función
    comment_id = comment_controller.create_comment(user_id=1, content="Another test comment", post_id=123)

    # Verificaciones
    mock_cursor.execute.assert_called_once_with(
        "SELECT create_comment(%s, %s, %s, %s)",
        (1, "Another test comment", 123, None)
    )
    # No se debe llamar a la notificación
    mock_create_notification.assert_not_called()
    assert comment_id == 2

def test_get_comments(mocker):
    # Mock de la conexión a la base de datos y la consulta
    mock_conn = mocker.patch('controllers.comment_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    # Datos simulados de retorno de `cur.fetchall()`
    mock_cursor.fetchall.return_value = [
        (1, "First comment", None, None),
        (2, "Second comment", None, None)
    ]

    # Ejecuta la función
    comments = comment_controller.get_comments(post_id=123)

    # Verificaciones
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_comments(%s, %s)", (123, None)
    )
    assert len(comments) == 2
    assert isinstance(comments[0], Comment)
    print(comments[1].content)
    print(comments[0].content)
    
    assert comments[0].content == "First comment"
    assert comments[1].content == "Second comment"

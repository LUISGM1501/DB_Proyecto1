import pytest
from controllers import post_controller
from models.post import Post

def test_create_post(mocker):
    mock_conn = mocker.patch('controllers.post_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    post_id = post_controller.create_post(
        user_id=1,
        content="Test content"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_post(%s, %s)",
        (1, "Test content")
    )
    assert post_id == 1

def test_get_post(mocker):
    mock_cache = mocker.patch('controllers.post_controller.get_cached_post', return_value=None)
    mock_conn = mocker.patch('controllers.post_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "Test content")

    mock_cache_post = mocker.patch('controllers.post_controller.cache_post')

    post = post_controller.get_post(post_id=1)

    mock_cache.assert_called_once_with(1)
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_post_by_id(%s)", (1,)
    )
    mock_cache_post.assert_called_once()
    assert isinstance(post, Post)
    assert post.content == "Test content"

def test_get_posts_paginated(mocker):
    mock_conn = mocker.patch('controllers.post_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Test content 1", 2),
        (1, "Test content 2", 2)
    ]

    posts, total_count = post_controller.get_posts_paginated(page=1, page_size=2)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_posts_paginated(%s, %s)", (1, 2)
    )
    assert len(posts) == 2
    assert total_count == 2
    assert isinstance(posts[0], Post)
    assert posts[0].content == "Test content 1"

# def test_update_post(mocker):
#     # Mock de 'redis_client' para evitar conexión real con Redis
#     mock_redis_client = mocker.patch('services.cache_service.redis_client')
#     # Mock de la conexión a la base de datos
#     mock_conn = mocker.patch('controllers.post_controller.get_postgres_connection')
#     mock_cursor = mocker.Mock()
#     mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

#     # Simula el retorno de `cur.fetchone()` con el ID del post actualizado
#     mock_cursor.fetchone.return_value = [1]

#     # Ejecuta la función
#     updated_post_id = post_controller.update_post(
#         post_id=1,
#         content="Updated content"
#     )

#     # Verificaciones
#     mock_cursor.execute.assert_called_once_with(
#         "SELECT update_post(%s, %s)", (1, "Updated content")
#     )
#     mock_redis_client.setex.assert_called()  # Verifica que se haya intentado actualizar el cache
#     assert updated_post_id == 1

def test_delete_post(mocker):
    mock_cache = mocker.patch('controllers.post_controller.cache_post')
    mock_conn = mocker.patch('controllers.post_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    deleted_post_id = post_controller.delete_post(post_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT delete_post(%s)", (1,)
    )
    mock_cache.assert_called_once_with(1, None, expire_time=1)
    assert deleted_post_id == 1

import pytest
from flask import Flask, jsonify
from flask_jwt_extended import create_access_token
from app import app
from controllers import comment_controller
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

# Prueba de integración para crear un comentario
@patch('controllers.comment_controller.create_comment')
def test_create_comment(mock_create_comment, client):
    mock_create_comment.return_value = 1

    access_token = create_access_token(identity=1)

    data = {
        'user_id': 1,
        'content': 'Test comment',
        'post_id': 1
    }

    response = client.post(
        '/comments',
        json=data,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 201
    assert response.json == {"message": "Comment created successfully", "comment_id": 1}
    mock_create_comment.assert_called_once_with(1, 'Test comment', 1, None)

# Prueba de integración para obtener comentarios
@patch('controllers.comment_controller.get_comments')
def test_get_comments(mock_get_comments, client):
    mock_get_comments.return_value = [
        {
            'id': 1,
            'user_id': 1,
            'content': 'Test comment',
            'post_id': 1,
            'place_id': None
        },
        {
            'id': 2,
            'user_id': 2,
            'content': 'Another comment',
            'post_id': 1,
            'place_id': None
        }
    ]

    access_token = create_access_token(identity=1)

    response = client.get(
        '/comments',
        headers={'Authorization': f'Bearer {access_token}'},
        query_string={'post_id': 1}
    )

    assert response.status_code == 200
    assert response.json == [
        {
            'id': 1,
            'user_id': 1,
            'content': 'Test comment',
            'post_id': 1,
            'place_id': None
        },
        {
            'id': 2,
            'user_id': 2,
            'content': 'Another comment',
            'post_id': 1,
            'place_id': None
        }
    ]
    
    mock_get_comments.assert_called_once_with("1", None)

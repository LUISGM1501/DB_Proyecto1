from unittest.mock import patch
import pytest
from flask_jwt_extended import create_access_token
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.reaction_controller.add_or_update_reaction')
def test_add_or_update_reaction(mock_add_or_update_reaction, client):
    mock_add_or_update_reaction.return_value = True

    with app.app_context():
        access_token = create_access_token(identity="1")  # Cambiado a string

    response = client.post(
        '/reactions',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'user_id': 1,
            'post_id': 1,
            'reaction_type': 'like'
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Reaction added/updated successfully"

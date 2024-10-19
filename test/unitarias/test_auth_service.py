# tests/unit/test_auth_service.py
import pytest
from unittest.mock import patch
from flask_jwt_extended import decode_token
from werkzeug.security import generate_password_hash
from services.auth_service import authenticate_user
from app import app

def test_authenticate_user_success(mocker):
    mock_user = mocker.Mock()
    mock_user.id = 1
    mock_user.password = generate_password_hash("correct_password")
    mock_get_user = mocker.patch('controllers.user_controller.get_user_by_username', return_value=mock_user)
    
    mock_create_access_token = mocker.patch('services.auth_service.create_access_token', return_value="test_token")
    access_token = authenticate_user("username", "correct_password")
    
    mock_get_user.assert_called_once_with("username")
    mock_create_access_token.assert_called_once_with(identity=1)
    assert access_token == "test_token"

def test_authenticate_user_invalid_password(mocker):
    mock_user = mocker.Mock()
    mock_user.password = generate_password_hash("correct_password")
    mock_get_user = mocker.patch('controllers.user_controller.get_user_by_username', return_value=mock_user)
    
    access_token = authenticate_user("username", "wrong_password")
    
    mock_get_user.assert_called_once_with("username")
    
    assert access_token is None

def test_authenticate_user_user_not_found(mocker):
    mock_get_user = mocker.patch('controllers.user_controller.get_user_by_username', return_value=None)
    
    access_token = authenticate_user("unknown_user", "any_password")
    
    mock_get_user.assert_called_once_with("unknown_user")
    
    assert access_token is None

def test_authenticate_user_success_token_verification(mocker):
    mock_user = mocker.Mock()
    mock_user.id = 1
    mock_user.password = generate_password_hash("correct_password")
    mock_get_user = mocker.patch('controllers.user_controller.get_user_by_username', return_value=mock_user)
    
    
    with app.app_context():
        app.config['JWT_SECRET_KEY'] = 'super-secret-key-for-testing'
        
        access_token = authenticate_user("username", "correct_password")
        
        mock_get_user.assert_called_once_with("username")
        
        decoded_token = decode_token(access_token)
        
        assert decoded_token['sub'] == 1  
        assert 'exp' in decoded_token      
        assert 'iat' in decoded_token      
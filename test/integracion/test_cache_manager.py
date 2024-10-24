# tests/integration/test_cache_manager.py
from src.services.cache_manager import CacheManager
import pytest

@pytest.fixture
def cache_manager():
    return CacheManager()

def test_get_or_cache_post_integration(cache_manager):
    def mock_fetch(post_id):
        return {'id': post_id, 'content': 'Test content'}
    
    # Primera llamada - debería buscar y cachear
    result1 = cache_manager.get_or_cache_post(1, mock_fetch)
    assert result1['content'] == 'Test content'
    
    # Segunda llamada - debería obtener del caché
    result2 = cache_manager.get_or_cache_post(1, mock_fetch)
    assert result2['content'] == 'Test content'

def test_manage_user_session_integration(cache_manager):
    session_data = {
        'user_id': 1,
        'username': 'test_user',
        'email': 'test@example.com'
    }
    
    # Crear sesión
    success = cache_manager.manage_user_session(1, session_data)
    assert success is True
    
    # Validar sesión
    session = cache_manager.validate_session(1)
    assert session is not None
    assert session['username'] == 'test_user'
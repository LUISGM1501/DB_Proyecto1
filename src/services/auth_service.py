# services/auth_service.py
from typing import Optional
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from controllers import user_controller
from services.cache_manager import CacheManager
from datetime import datetime

def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Autentica un usuario y devuelve un token de acceso.
    """
    user = user_controller.get_user_by_username(username)
    if user and check_password_hash(user.password, password):
        return create_access_token(identity=user.id)
    return None

class AuthService:
    def __init__(self):
        self.cache_manager = CacheManager()

    def manage_session(self, user_id: int, username: str, access_token: str) -> None:
        """
        Gestiona la sesión del usuario.
        """
        session_data = {
            'user_id': user_id,
            'username': username,
            'last_login': datetime.utcnow().isoformat(),
            'access_token': access_token
        }
        self.cache_manager.manage_user_session(user_id, session_data)

    def validate_session(self, user_id: int) -> bool:
        """
        Valida la sesión de un usuario.
        """
        session = self.cache_manager.validate_session(user_id)
        return bool(session)

    def logout_user(self, user_id: int) -> bool:
        """
        Cierra la sesión de un usuario.
        """
        return self.cache_manager.redis_service.delete_user_session(user_id)

    def check_rate_limit(self, user_id: int, action: str) -> bool:
        """
        Verifica límites de tasa para acciones específicas.
        """
        limits = {
            'login': 5,        # 5 intentos por hora
            'post': 50,        # 50 posts por hora
            'comment': 100,    # 100 comentarios por hora
            'like': 200        # 200 likes por hora
        }
        return self.cache_manager.check_rate_limit(user_id, action, limits.get(action, 100))
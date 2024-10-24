# services/redis_service.py
from typing import Dict, List, Optional, Union
import json
from datetime import datetime, timedelta
from config.database import get_redis_connection

class RedisService:
    def __init__(self):
        self._redis_client = get_redis_connection()
        self.default_expire = 3600  # 1 hora por defecto

    @property
    def redis_client(self):
        return self._redis_client

    def _serialize(self, data: Union[Dict, List]) -> str:
        """Serializa datos para almacenamiento en Redis."""
        return json.dumps(data, default=str)

    def _deserialize(self, data: str) -> Union[Dict, List, None]:
        """Deserializa datos desde Redis."""
        try:
            return json.loads(data) if data else None
        except (TypeError, json.JSONDecodeError):
            return None

    def cache_post(self, post_id: int, post_data: Dict, expire_time: int = None) -> bool:
        """Almacena un post en caché."""
        key = f"post:{post_id}"
        return self.redis_client.setex(
            key,
            expire_time or self.default_expire,
            self._serialize(post_data)
        )

    def get_cached_post(self, post_id: int) -> Optional[Dict]:
        """Recupera un post del caché."""
        key = f"post:{post_id}"
        data = self.redis_client.get(key)
        return self._deserialize(data)

    def update_popular_posts(self, posts: List[Dict], expire_time: int = None) -> bool:
        """Actualiza la lista de posts populares."""
        return self.redis_client.setex(
            "popular_posts",
            expire_time or self.default_expire,
            self._serialize(posts)
        )

    def get_popular_posts(self) -> Optional[List[Dict]]:
        """Obtiene la lista de posts populares."""
        data = self.redis_client.get("popular_posts")
        return self._deserialize(data)

    def cache_post_comments(self, post_id: int, comments: List[Dict], expire_time: int = None) -> bool:
        """Almacena los comentarios de un post en caché."""
        key = f"comments:{post_id}"
        return self.redis_client.setex(
            key,
            expire_time or self.default_expire,
            self._serialize(comments)
        )

    def get_cached_comments(self, post_id: int) -> Optional[List[Dict]]:
        """Recupera los comentarios de un post del caché."""
        key = f"comments:{post_id}"
        data = self.redis_client.get(key)
        return self._deserialize(data)

    def create_user_session(self, user_id: int, session_data: Dict, expire_time: int = 86400) -> bool:
        """Crea una sesión de usuario."""
        key = f"session:{user_id}"
        session_data['created_at'] = datetime.utcnow().isoformat()
        return self.redis_client.setex(
            key,
            expire_time,  # 24 horas por defecto
            self._serialize(session_data)
        )

    def get_user_session(self, user_id: int) -> Optional[Dict]:
        """Recupera la sesión de un usuario."""
        key = f"session:{user_id}"
        data = self.redis_client.get(key)
        return self._deserialize(data)

    def delete_user_session(self, user_id: int) -> bool:
        """Elimina la sesión de un usuario."""
        key = f"session:{user_id}"
        return bool(self.redis_client.delete(key))

    def check_rate_limit(self, user_id: int, action: str, limit: int, window: int = 3600) -> bool:
        """
        Verifica si un usuario ha excedido el límite de acciones.
        Returns True si está dentro del límite, False si lo excedió.
        """
        key = f"rate_limit:{user_id}:{action}"
        current = self.redis_client.get(key)
        
        if not current:
            self.redis_client.setex(key, window, 1)
            return True
            
        count = int(current)
        if count >= limit:
            return False
            
        self.redis_client.incr(key)
        return True

    def clear_expired_sessions(self) -> int:
        """Limpia sesiones expiradas y retorna el número de sesiones eliminadas."""
        pattern = "session:*"
        cleared = 0
        for key in self.redis_client.scan_iter(pattern):
            if not self.redis_client.ttl(key):
                self.redis_client.delete(key)
                cleared += 1
        return cleared
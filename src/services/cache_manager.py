# services/cache_manager.py
from typing import List, Dict, Optional
from services.redis_service import RedisService
from services.redis_metrics import RedisMetrics
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self):
        self.redis_service = RedisService()
        self.metrics = RedisMetrics()

    def get_or_cache_post(self, post_id: int, fetch_function) -> Optional[Dict]:
        """
        Obtiene un post del caché o lo busca y cachea si no existe.
        """
        cached_post = self.redis_service.get_cached_post(post_id)
        if cached_post:
            self.metrics.record_cache_hit('posts')
            return cached_post

        self.metrics.record_cache_miss('posts')
        post_data = fetch_function(post_id)
        if post_data:
            self.redis_service.cache_post(post_id, post_data)
        return post_data

    def update_popular_posts(self, posts: List[Dict]) -> None:
        """
        Actualiza el caché de posts populares.
        """
        self.redis_service.update_popular_posts(posts)

    def get_post_comments(self, post_id: int, fetch_function) -> List[Dict]:
        """
        Obtiene comentarios del caché o los busca y cachea si no existen.
        """
        cached_comments = self.redis_service.get_cached_comments(post_id)
        if cached_comments:
            self.metrics.record_cache_hit('comments')
            return cached_comments

        self.metrics.record_cache_miss('comments')
        comments = fetch_function(post_id)
        if comments:
            self.redis_service.cache_post_comments(post_id, comments)
        return comments

    def manage_user_session(self, user_id: int, session_data: Dict) -> bool:
        """
        Gestiona la sesión de un usuario.
        """
        success = self.redis_service.create_user_session(user_id, session_data)
        if success:
            self.metrics.record_cache_hit('sessions')
        else:
            self.metrics.record_cache_miss('sessions')
        return success

    def validate_session(self, user_id: int) -> Optional[Dict]:
        """
        Valida y retorna la sesión de un usuario si existe y es válida.
        """
        session = self.redis_service.get_user_session(user_id)
        if not session:
            return None

        created_at = datetime.fromisoformat(session['created_at'])
        if datetime.utcnow() - created_at > timedelta(days=1):
            self.redis_service.delete_user_session(user_id)
            return None

        return session

    def check_rate_limit(self, user_id: int, action: str, limit: int) -> bool:
        """
        Verifica límites de tasa para acciones específicas.
        """
        return self.redis_service.check_rate_limit(user_id, action, limit)

    def invalidate_cache(self, post_id: int) -> None:
        """
        Invalida el caché para un post específico.
        """
        self.redis_service.cache_post(post_id, None, expire_time=1)

    def get_cache_statistics(self) -> Dict:
        """
        Obtiene estadísticas completas del sistema de caché.
        """
        return {
            'general_stats': self.metrics.generate_daily_report(),
            'memory_usage': self.metrics.get_memory_usage(),
            'key_statistics': self.metrics.get_key_statistics()
        }
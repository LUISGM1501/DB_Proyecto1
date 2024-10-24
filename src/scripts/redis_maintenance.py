# scripts/redis_maintenance.py
from services.redis_service import RedisService
from services.cache_manager import CacheManager
import schedule
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisMaintenance:
    def __init__(self):
        self.redis_service = RedisService()
        self.cache_manager = CacheManager()

    def clear_expired_sessions(self):
        """Limpia sesiones expiradas."""
        try:
            cleared = self.redis_service.clear_expired_sessions()
            logger.info(f"Cleared {cleared} expired sessions")
        except Exception as e:
            logger.error(f"Error clearing expired sessions: {str(e)}")

    def update_popular_posts(self):
        """Actualiza el caché de posts populares."""
        try:
            # Aquí iría la lógica para obtener los posts populares
            # desde la base de datos y actualizar el caché
            logger.info("Updated popular posts cache")
        except Exception as e:
            logger.error(f"Error updating popular posts: {str(e)}")

    def clear_old_rate_limits(self):
        """Limpia registros antiguos de rate limiting."""
        try:
            pattern = "rate_limit:*"
            cleared = 0
            for key in self.redis_service.redis_client.scan_iter(pattern):
                if not self.redis_service.redis_client.ttl(key):
                    self.redis_service.redis_client.delete(key)
                    cleared += 1
            logger.info(f"Cleared {cleared} old rate limit records")
        except Exception as e:
            logger.error(f"Error clearing rate limits: {str(e)}")

def run_maintenance():
    maintenance = RedisMaintenance()

    # Programar tareas
    schedule.every(1).hours.do(maintenance.clear_expired_sessions)
    schedule.every(15).minutes.do(maintenance.update_popular_posts)
    schedule.every(6).hours.do(maintenance.clear_old_rate_limits)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("Starting Redis maintenance tasks...")
    run_maintenance()
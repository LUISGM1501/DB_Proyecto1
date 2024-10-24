# services/redis_metrics.py
from datetime import datetime, timedelta
from typing import Dict, List
from services.redis_service import RedisService
import logging

logger = logging.getLogger(__name__)

class RedisMetrics:
    def __init__(self):
        self.redis_service = RedisService()
        self.redis_client = self.redis_service.redis_client

    def record_cache_hit(self, cache_type: str):
        """Registra un hit de caché."""
        day_key = f"metrics:hits:{cache_type}:{datetime.now().date()}"
        self.redis_client.incr(day_key)
        self.redis_client.expire(day_key, 86400 * 7)  # Guardar por 7 días

    def record_cache_miss(self, cache_type: str):
        """Registra un miss de caché."""
        day_key = f"metrics:misses:{cache_type}:{datetime.now().date()}"
        self.redis_client.incr(day_key)
        self.redis_client.expire(day_key, 86400 * 7)  # Guardar por 7 días

    def get_cache_stats(self, cache_type: str, days: int = 7) -> Dict:
        """Obtiene estadísticas de caché para un período específico."""
        total_hits = 0
        total_misses = 0
        daily_stats = []

        for i in range(days):
            date = datetime.now().date() - timedelta(days=i)
            hits_key = f"metrics:hits:{cache_type}:{date}"
            misses_key = f"metrics:misses:{cache_type}:{date}"

            hits = int(self.redis_client.get(hits_key) or 0)
            misses = int(self.redis_client.get(misses_key) or 0)

            total_hits += hits
            total_misses += misses

            daily_stats.append({
                'date': date.isoformat(),
                'hits': hits,
                'misses': misses,
                'ratio': hits / (hits + misses) if hits + misses > 0 else 0
            })

        total_requests = total_hits + total_misses
        hit_ratio = total_hits / total_requests if total_requests > 0 else 0

        return {
            'cache_type': cache_type,
            'total_hits': total_hits,
            'total_misses': total_misses,
            'hit_ratio': hit_ratio,
            'daily_stats': daily_stats
        }

    def get_memory_usage(self) -> Dict:
        """Obtiene estadísticas de uso de memoria de Redis."""
        info = self.redis_client.info('memory')
        return {
            'used_memory': info['used_memory_human'],
            'peak_memory': info['used_memory_peak_human'],
            'fragmentation_ratio': info['mem_fragmentation_ratio']
        }

    def get_key_statistics(self) -> Dict:
        """Obtiene estadísticas sobre los tipos de keys en Redis."""
        stats = {
            'posts': 0,
            'comments': 0,
            'sessions': 0,
            'rate_limits': 0
        }

        for key in self.redis_client.scan_iter("*"):
            if 'post:' in key:
                stats['posts'] += 1
            elif 'comments:' in key:
                stats['comments'] += 1
            elif 'session:' in key:
                stats['sessions'] += 1
            elif 'rate_limit:' in key:
                stats['rate_limits'] += 1

        return stats

    def generate_daily_report(self) -> Dict:
        """Genera un reporte diario completo de uso de Redis."""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'memory_usage': self.get_memory_usage(),
                'key_statistics': self.get_key_statistics(),
                'cache_stats': {
                    'posts': self.get_cache_stats('posts', 1),
                    'comments': self.get_cache_stats('comments', 1),
                    'sessions': self.get_cache_stats('sessions', 1)
                }
            }

            # Guardar el reporte en Redis
            report_key = f"metrics:daily_report:{datetime.now().date()}"
            self.redis_client.setex(
                report_key,
                86400 * 30,  # Guardar por 30 días
                self.redis_service._serialize(report)
            )

            return report
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            return {}
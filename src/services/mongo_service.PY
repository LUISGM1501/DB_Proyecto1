# services/mongo_service.py
from datetime import datetime, UTC
from typing import Dict, List, Optional
from bson import ObjectId
from config.database import get_mongo_connection

class MongoService:
    def __init__(self):
        self.db = get_mongo_connection()

    def create_travel_details(self, travel_data: Dict) -> str:
        """
        Almacena detalles extendidos de un viaje.
        """
        travel_data['created_at'] = datetime.now(UTC)
        try:
            result = self.db.travel_details.insert_one(travel_data)
            return str(result.inserted_id)
        except Exception as e:
            return None

    def get_travel_details(self, travel_id: str) -> Optional[Dict]:
        """
        Recupera detalles de un viaje específico.
        """
        return self.db.travel_details.find_one({'_id': ObjectId(travel_id)})

    def create_user_stats(self, user_id: int) -> str:
        """
        Inicializa estadísticas para un nuevo usuario.
        """
        stats_data = {
            'user_id': user_id,
            'total_posts': 0,
            'total_likes_received': 0,
            'total_comments_received': 0,
            'places_visited': [],
            'countries_visited': set(),
            'created_at': datetime.now(UTC),
            'last_updated': datetime.now(UTC)
        }
        result = self.db.user_stats.insert_one(stats_data)
        return str(result.inserted_id)

    def update_user_stats(self, user_id: int, update_data: Dict) -> bool:
        """
        Actualiza las estadísticas de un usuario.
        """
        update_data['last_updated'] = datetime.now(UTC)
        result = self.db.user_stats.update_one(
            {'user_id': user_id},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def create_activity_log(self, user_id: int, activity_type: str, details: Dict) -> str:
        """
        Registra una actividad de usuario.
        """
        log_data = {
            'user_id': user_id,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.now(UTC)
        }
        result = self.db.activity_logs.insert_one(log_data)
        return str(result.inserted_id)

    def get_user_activity_logs(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Obtiene los registros de actividad de un usuario.
        """
        return list(
            self.db.activity_logs.find(
                {'user_id': user_id}
            ).sort('timestamp', -1).limit(limit)
        )

    def create_place_review(self, place_id: int, user_id: int, review_data: Dict) -> str:
        """
        Almacena una reseña detallada de un lugar.
        """
        review_data.update({
            'place_id': place_id,
            'user_id': user_id,
            'created_at': datetime.now(UTC),
            'updated_at': datetime.now(UTC)
        })
        result = self.db.place_reviews.insert_one(review_data)
        return str(result.inserted_id)

    def get_place_reviews(self, place_id: int, limit: int = 10) -> List[Dict]:
        """
        Obtiene las reseñas de un lugar específico.
        """
        return list(
            self.db.place_reviews.find(
                {'place_id': place_id}
            ).sort('created_at', -1).limit(limit)
        )

    def store_media_links(self, reference_id: int, reference_type: str, media_links: List[Dict]) -> str:
        """
        Almacena links de media asociados a posts o lugares.
        """
        media_data = {
            'reference_id': reference_id,
            'reference_type': reference_type,
            'links': media_links,
            'created_at': datetime.now(UTC)
        }
        result = self.db.media_links.insert_one(media_data)
        return str(result.inserted_id)

    def get_media_links(self, reference_id: int, reference_type: str) -> Optional[Dict]:
        """
        Recupera links de media asociados a un post o lugar.
        """
        return self.db.media_links.find_one({
            'reference_id': reference_id,
            'reference_type': reference_type
        })
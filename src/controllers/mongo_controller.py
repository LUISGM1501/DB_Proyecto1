# controllers/mongo_controller.py
from services.mongo_service import MongoService
from typing import Dict, List, Optional

class MongoController:
    def __init__(self):
        self.mongo_service = MongoService()

    def create_travel_record(self, user_id: int, travel_data: Dict) -> Dict:
        """
        Crea un registro completo de viaje con todos sus detalles.
        """
        try:
            # Enriquecer los datos del viaje
            enriched_travel_data = {
                'user_id': user_id,
                'title': travel_data.get('title'),
                'description': travel_data.get('description'),
                'places': travel_data.get('places', []),
                'start_date': travel_data.get('start_date'),
                'end_date': travel_data.get('end_date'),
                'budget': travel_data.get('budget'),
                'expenses': travel_data.get('expenses', []),
                'itinerary': travel_data.get('itinerary', []),
                'tips': travel_data.get('tips', []),
                'photos': travel_data.get('photos', []),
                'status': 'active'
            }
            
            # Almacenar en MongoDB
            travel_id = self.mongo_service.create_travel_details(enriched_travel_data)
            
            # Actualizar estadísticas del usuario
            self.update_user_travel_stats(user_id, enriched_travel_data)
            
            # Registrar la actividad
            self.mongo_service.create_activity_log(
                user_id=user_id,
                activity_type='travel_created',
                details={'travel_id': travel_id}
            )
            
            return {'travel_id': travel_id, 'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_user_travel_stats(self, user_id: int, travel_data: Dict) -> None:
        """
        Actualiza las estadísticas de viaje del usuario.
        """
        stats_update = {
            '$inc': {'total_travels': 1},
            '$push': {
                'visited_places': {'$each': [place['id'] for place in travel_data.get('places', [])]},
                'visited_countries': {'$each': list(set(place['country'] for place in travel_data.get('places', [])))},
            }
        }
        self.mongo_service.update_user_stats(user_id, stats_update)

    def create_detailed_review(self, user_id: int, place_id: int, review_data: Dict) -> Dict:
        """
        Crea una reseña detallada de un lugar.
        """
        try:
            # Enriquecer los datos de la reseña
            enriched_review = {
                'rating': review_data.get('rating'),
                'detailed_text': review_data.get('text'),
                'visit_date': review_data.get('visit_date'),
                'recommendations': review_data.get('recommendations', []),
                'tips': review_data.get('tips', []),
                'photos': review_data.get('photos', []),
                'categories': review_data.get('categories', []),
                'price_level': review_data.get('price_level'),
                'visited_with': review_data.get('visited_with'),
                'highlights': review_data.get('highlights', [])
            }
            
            review_id = self.mongo_service.create_place_review(place_id, user_id, enriched_review)
            
            # Registrar la actividad
            self.mongo_service.create_activity_log(
                user_id=user_id,
                activity_type='review_created',
                details={'place_id': place_id, 'review_id': review_id}
            )
            
            return {'review_id': review_id, 'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_user_activity_summary(self, user_id: int) -> Dict:
        """
        Obtiene un resumen de la actividad del usuario.
        """
        try:
            # Obtener estadísticas
            stats = self.mongo_service.db.user_stats.find_one({'user_id': user_id})
            
            # Obtener últimas actividades
            recent_activities = self.mongo_service.get_user_activity_logs(user_id, limit=5)
            
            return {
                'stats': stats,
                'recent_activities': recent_activities,
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
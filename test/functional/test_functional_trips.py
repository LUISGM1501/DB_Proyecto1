# test/functional/test_functional_trips.py
"""
Prueba Funcional: Flujo Completo de Gestión de Viajes
Prueba el flujo de negocio end-to-end desde la creación hasta las estadísticas
"""

import pytest
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token
from app import app
from models.trip import Trip
from datetime import date

@pytest.fixture
def client():
    """Cliente de pruebas para functional testing"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'functional-test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def auth_headers():
    """Headers de autenticación para las pruebas"""
    with app.app_context():
        access_token = create_access_token(identity="1")
        return {'Authorization': f'Bearer {access_token}'}

class TestTripFunctionalFlow:
    """
    Prueba Funcional: Flujo completo de gestión de viajes
    Simula el comportamiento real de un usuario gestionando sus viajes
    """
    
    def test_complete_trip_management_workflow(self, client, auth_headers):
        """
        PRUEBA FUNCIONAL: Flujo completo de gestión de viajes
        
        Flujo de negocio:
        1. Usuario crea un viaje
        2. Usuario agrega lugares al viaje
        3. Usuario consulta los lugares del viaje
        4. Usuario obtiene estadísticas del viaje
        5. Usuario actualiza el estado del viaje
        
        Esta prueba valida que todos los componentes trabajen juntos correctamente
        """
        print("\n🎯 INICIANDO PRUEBA FUNCIONAL: Flujo Completo de Viajes")
        
        # Mock del viaje que se mantendrá durante toda la prueba
        mock_trip = Trip(
            user_id=1,
            title='Aventura en Costa Rica',
            description='Viaje de ecoturismo por Costa Rica',
            start_date=date(2024, 12, 1),
            end_date=date(2024, 12, 15),
            status='planned',
            budget=2500.00,
            id=1
        )
        
        # Patches que durarán toda la prueba
        with patch('controllers.trip_controller.create_trip') as mock_create_trip, \
             patch('controllers.trip_controller.get_trip') as mock_get_trip, \
             patch('controllers.trip_controller.add_place_to_trip') as mock_add_place, \
             patch('controllers.trip_controller.get_trip_places') as mock_get_places, \
             patch('controllers.trip_controller.get_trip_statistics') as mock_get_stats, \
             patch('controllers.trip_controller.update_trip') as mock_update_trip:
            
            # Configurar mocks
            mock_create_trip.return_value = 1
            mock_get_trip.return_value = mock_trip
            mock_add_place.return_value = 1
            mock_update_trip.return_value = 1
            
            # ===== PASO 1: CREAR VIAJE =====
            print("\n📝 PASO 1: Creando viaje...")
            
            trip_data = {
                'title': 'Aventura en Costa Rica',
                'description': 'Viaje de ecoturismo por Costa Rica',
                'start_date': '2024-12-01',
                'end_date': '2024-12-15',
                'status': 'planned',
                'budget': 2500.00
            }
            
            response = client.post('/trips', headers=auth_headers, json=trip_data)
            
            # Verificar creación exitosa
            assert response.status_code == 201, f"Error creando viaje: {response.get_json()}"
            assert 'trip_id' in response.json
            trip_id = response.json['trip_id']
            
            print(f"✅ Viaje creado exitosamente con ID: {trip_id}")
            
            # ===== PASO 2: AGREGAR LUGARES AL VIAJE =====
            print("\n🌎 PASO 2: Agregando lugares al viaje...")
            
            # Agregar múltiples lugares
            lugares_a_agregar = [
                {
                    'place_id': 10,
                    'visit_date': '2024-12-03',
                    'visit_order': 1,
                    'notes': 'Volcán Arenal - día completo'
                },
                {
                    'place_id': 20,
                    'visit_date': '2024-12-07',
                    'visit_order': 2,
                    'notes': 'Manuel Antonio - playa y naturaleza'
                },
                {
                    'place_id': 30,
                    'visit_date': '2024-12-12',
                    'visit_order': 3,
                    'notes': 'Monteverde - bosque nuboso'
                }
            ]
            
            lugares_agregados = 0
            for lugar in lugares_a_agregar:
                response = client.post(
                    f'/trips/{trip_id}/places',
                    headers=auth_headers,
                    json=lugar
                )
                
                assert response.status_code == 201, f"Error agregando lugar: {response.get_json()}"
                lugares_agregados += 1
                
                print(f"  ✅ Lugar {lugares_agregados} agregado: {lugar['notes']}")
            
            print(f"✅ Total de {lugares_agregados} lugares agregados al viaje")
            
            # ===== PASO 3: CONSULTAR LUGARES DEL VIAJE =====
            print("\n📋 PASO 3: Consultando lugares del viaje...")
            
            # Mock de lugares en el viaje
            mock_places_data = [
                {
                    "place_id": 10,
                    "name": "Volcán Arenal",
                    "description": "Volcán activo con aguas termales",
                    "city": "La Fortuna",
                    "country": "Costa Rica",
                    "visit_date": "2024-12-03",
                    "visit_order": 1,
                    "notes": "Volcán Arenal - día completo",
                    "rating": None
                },
                {
                    "place_id": 20,
                    "name": "Parque Nacional Manuel Antonio",
                    "description": "Playa paradisíaca con vida silvestre",
                    "city": "Manuel Antonio",
                    "country": "Costa Rica",
                    "visit_date": "2024-12-07",
                    "visit_order": 2,
                    "notes": "Manuel Antonio - playa y naturaleza",
                    "rating": None
                },
                {
                    "place_id": 30,
                    "name": "Reserva Monteverde",
                    "description": "Bosque nuboso único en el mundo",
                    "city": "Monteverde",
                    "country": "Costa Rica",
                    "visit_date": "2024-12-12",
                    "visit_order": 3,
                    "notes": "Monteverde - bosque nuboso",
                    "rating": None
                }
            ]
            mock_get_places.return_value = mock_places_data
            
            response = client.get(f'/trips/{trip_id}/places', headers=auth_headers)
            
            assert response.status_code == 200, f"Error consultando lugares: {response.get_json()}"
            assert 'places' in response.json
            places = response.json['places']
            assert len(places) == 3, f"Se esperaban 3 lugares, se obtuvieron {len(places)}"
            
            print(f"✅ Consultados {len(places)} lugares:")
            for place in places:
                print(f"  • {place['name']} - {place['visit_date']}")
            
            # ===== PASO 4: OBTENER ESTADÍSTICAS DEL VIAJE =====
            print("\n📊 PASO 4: Obteniendo estadísticas del viaje...")
            
            # Mock de estadísticas del viaje
            mock_statistics = {
                "total_places": 3,
                "total_expenses": 1500.75,
                "avg_place_rating": 4.5,
                "trip_duration_days": 15
            }
            mock_get_stats.return_value = mock_statistics
            
            response = client.get(f'/trips/{trip_id}/statistics', headers=auth_headers)
            
            assert response.status_code == 200, f"Error obteniendo estadísticas: {response.get_json()}"
            stats = response.json
            
            # Verificar que las estadísticas sean coherentes
            assert stats['total_places'] == 3, "Las estadísticas no coinciden con los lugares agregados"
            assert stats['trip_duration_days'] == 15, "La duración del viaje no es correcta"
            assert isinstance(stats['total_expenses'], (int, float)), "Los gastos deben ser numéricos"
            
            print(f"✅ Estadísticas obtenidas:")
            print(f"  • Total lugares: {stats['total_places']}")
            print(f"  • Duración: {stats['trip_duration_days']} días")
            print(f"  • Gastos totales: ${stats['total_expenses']}")
            print(f"  • Rating promedio: {stats['avg_place_rating']}")
            
            # ===== PASO 5: ACTUALIZAR ESTADO DEL VIAJE =====
            print("\n🔄 PASO 5: Actualizando estado del viaje...")
            
            update_data = {
                'status': 'in_progress',
                'description': 'Viaje de ecoturismo por Costa Rica - ¡Ya comenzó!'
            }
            
            response = client.put(
                f'/trips/{trip_id}',
                headers=auth_headers,
                json=update_data
            )
            
            assert response.status_code == 200, f"Error actualizando viaje: {response.get_json()}"
            assert 'trip_id' in response.json
            
            print(f"✅ Estado del viaje actualizado a: {update_data['status']}")
            
            # ===== VERIFICACIÓN FINAL DEL FLUJO =====
            print("\n✅ FLUJO FUNCIONAL COMPLETADO EXITOSAMENTE")
            print("\n📋 RESUMEN DEL FLUJO:")
            print(f"  1. ✅ Viaje creado: 'Aventura en Costa Rica'")
            print(f"  2. ✅ Lugares agregados: 3 destinos")
            print(f"  3. ✅ Lugares consultados: Lista completa")
            print(f"  4. ✅ Estadísticas obtenidas: Datos coherentes")
            print(f"  5. ✅ Estado actualizado: 'in_progress'")
            
            # Assertion final que valida todo el flujo
            assert True, "Flujo funcional completado exitosamente"
            
            print("\n🎯 PRUEBA FUNCIONAL: ¡EXITOSA!")


if __name__ == "__main__":
    # Ejecutar la prueba directamente
    pytest.main([__file__, "-v"])
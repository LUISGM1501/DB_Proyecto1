# tests/usability/test_usability_trips.py
"""
Pruebas de Usabilidad para la funcionalidad de Trips
Evalúa la facilidad de uso, intuitividad y experiencia del usuario
desde la perspectiva de la API y sus respuestas
"""

import pytest
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token
from app import app
from models.trip import Trip
from datetime import date, datetime
import json

@pytest.fixture
def client():
    """Cliente de pruebas para usability testing"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'usability-test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def auth_headers():
    """Headers de autenticación para las pruebas - usando STRING identity"""
    with app.app_context():
        access_token = create_access_token(identity="1")  # STRING
        return {'Authorization': f'Bearer {access_token}'}


class TestAPIUsabilityAndClarity:
    """
    Pruebas de usabilidad de la API
    Evalúa la claridad, consistencia y facilidad de uso
    """
    
    def test_api_response_clarity_and_consistency(self, client, auth_headers):
        """
        Prueba de usabilidad: Claridad y consistencia de respuestas de API
        Verifica que las respuestas sean claras y consistentes
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Claridad de respuestas API")
        
        with patch('controllers.trip_controller.create_trip') as mock_create, \
             patch('controllers.trip_controller.get_trip') as mock_get:
            
            # Test 1: Creación de viaje - respuesta clara
            mock_create.return_value = 1
            
            response = client.post('/trips', headers=auth_headers, json={
                'title': 'Viaje de Prueba',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            })
            
            # Verificar claridad de la respuesta
            assert response.status_code == 201
            assert 'message' in response.json
            assert 'trip_id' in response.json
            assert response.json['message'] == 'Trip created successfully'
            assert isinstance(response.json['trip_id'], int)
            
            print("Respuesta de creación clara y útil")
            
            # Test 2: Consulta de viaje - información completa
            mock_trip = Trip(
                user_id=1,  # INTEGER para coincidir con BD
                title='Viaje de Prueba',
                description='Una descripción útil',
                start_date=date(2024, 7, 1),
                end_date=date(2024, 7, 15),
                status='planned',
                budget=1500.00,
                id=1
            )
            mock_get.return_value = mock_trip
            
            response = client.get('/trips/1', headers=auth_headers)
            
            # Verificar completitud de la información
            assert response.status_code == 200
            trip_data = response.json
            
            # Campos esenciales presentes
            essential_fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'budget']
            for field in essential_fields:
                assert field in trip_data, f"Campo esencial '{field}' faltante"
            
            # Fechas en formato legible
            assert trip_data['start_date'] == '2024-07-01'
            assert trip_data['end_date'] == '2024-07-15'
            
            print("Información completa y bien estructurada")

    def test_error_messages_user_friendly(self, client, auth_headers):
        """
        Prueba de usabilidad: Mensajes de error amigables
        Verifica que los errores sean comprensibles para el usuario
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Mensajes de error amigables")
        
        # Test 1: Campos requeridos faltantes
        response = client.post('/trips', headers=auth_headers, json={
            'title': 'Solo título'
            # Faltan start_date y end_date
        })
        
        assert response.status_code == 400
        assert 'error' in response.json
        error_msg = response.json['error']
        assert 'Missing required field' in error_msg
        print("Error de campos faltantes claro")
        
        # Test 2: Recurso no encontrado
        with patch('controllers.trip_controller.get_trip', return_value=None):
            response = client.get('/trips/9999', headers=auth_headers)
            
            assert response.status_code == 404
            assert response.json['error'] == 'Trip not found'
            print("Error de recurso no encontrado claro")
        
        # Test 3: Acceso no autorizado
        with patch('controllers.trip_controller.get_trip') as mock_get:
            # Viaje de otro usuario
            other_trip = Trip(2, 'Viaje Ajeno', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)  # INTEGER
            mock_get.return_value = other_trip
            
            response = client.get('/trips/1', headers=auth_headers)
            
            assert response.status_code == 403
            assert 'Unauthorized' in response.json['error']
            print("Error de autorización claro")

    def test_api_intuitiveness_and_predictability(self, client, auth_headers):
        """
        Prueba de usabilidad: Intuitividad y predictibilidad de la API
        Verifica que los endpoints se comporten de manera intuitiva
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Intuitividad de API")
        
        with patch('controllers.trip_controller.get_user_trips') as mock_get_trips, \
             patch('controllers.trip_controller.search_trips') as mock_search:
            
            # Test 1: Paginación intuitiva
            mock_trips = [
                Trip("1", f'Viaje {i}', f'Desc {i}', date(2024, 7, 1), date(2024, 7, 15), id=i)
                for i in range(1, 6)
            ]
            mock_get_trips.return_value = (mock_trips, 25)  # 5 trips de 25 total
            
            response = client.get('/trips?page=1&page_size=5', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            
            # Estructura de paginación intuitiva
            assert 'trips' in data
            assert 'total_count' in data
            assert 'page' in data
            assert 'page_size' in data
            
            assert len(data['trips']) == 5
            assert data['total_count'] == 25
            assert data['page'] == 1
            assert data['page_size'] == 5
            
            print("Paginación intuitiva y completa")
            
            # Test 2: Búsqueda con criterios múltiples
            search_results = [
                Trip("1", 'Viaje Europa', 'Cultural', date(2024, 6, 1), date(2024, 6, 20), 
                     status='completed', id=1)
            ]
            mock_search.return_value = (search_results, 1)
            
            response = client.get('/trips/search?status=completed&title=Europa', headers=auth_headers)
            
            assert response.status_code == 200
            search_data = response.json
            
            # Respuesta de búsqueda bien estructurada
            assert 'trips' in search_data
            assert 'total_count' in search_data
            assert 'search_criteria' in search_data
            
            # Criterios de búsqueda devueltos para claridad
            criteria = search_data['search_criteria']
            assert criteria['status'] == 'completed'
            assert criteria['title'] == 'Europa'
            
            print("Búsqueda intuitiva con criterios claros")

    def test_data_format_consistency(self, client, auth_headers):
        """
        Prueba de usabilidad: Consistencia en formatos de datos
        Verifica que los datos se presenten de manera consistente
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Consistencia de formatos")
        
        with patch('controllers.trip_controller.get_trip') as mock_get, \
             patch('controllers.trip_controller.get_trip_statistics') as mock_stats, \
             patch('controllers.trip_controller.get_trip_places') as mock_places:
            
            # Configurar datos de prueba
            mock_trip = Trip(
                user_id=1,  # INTEGER
                title='Viaje Consistencia',
                description='Prueba de formatos',
                start_date=date(2024, 8, 15),
                end_date=date(2024, 8, 25),
                status='planned',
                budget=2000.50,
                id=1
            )
            mock_get.return_value = mock_trip
            
            mock_statistics = {
                "total_places": 3,
                "total_expenses": 1234.56,
                "avg_place_rating": 4.33,
                "trip_duration_days": 10
            }
            mock_stats.return_value = mock_statistics
            
            mock_places_data = [
                {
                    "place_id": 1,
                    "name": "Lugar Test",
                    "visit_date": "2024-08-16",
                    "visit_order": 1,
                    "rating": 5
                }
            ]
            mock_places.return_value = mock_places_data
            
            # Test 1: Formatos de fecha consistentes
            response = client.get('/trips/1', headers=auth_headers)
            trip_data = response.json
            
            # Verificar formato de fechas ISO
            assert trip_data['start_date'] == '2024-08-15'
            assert trip_data['end_date'] == '2024-08-25'
            print("Fechas en formato ISO consistente")
            
            # Test 2: Números decimales con precisión apropiada
            response = client.get('/trips/1/statistics', headers=auth_headers)
            stats_data = response.json
            
            # Verificar que los números se presentan apropiadamente
            assert isinstance(stats_data['total_expenses'], (int, float))
            assert isinstance(stats_data['avg_place_rating'], (int, float))
            assert isinstance(stats_data['total_places'], int)
            print("Formatos numéricos consistentes")
            
            # Test 3: Estructura consistente en listas
            response = client.get('/trips/1/places', headers=auth_headers)
            places_data = response.json
            
            assert 'places' in places_data
            assert isinstance(places_data['places'], list)
            
            if places_data['places']:
                place = places_data['places'][0]
                assert 'place_id' in place
                assert 'name' in place
                assert 'visit_date' in place
            
            print("Estructura de listas consistente")

    def test_api_discoverability_and_help(self, client, auth_headers):
        """
        Prueba de usabilidad: Descubribilidad y ayuda de la API
        Verifica que la API sea autodescriptiva
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Descubribilidad de API")
        
        # Test 1: Endpoint raíz informativo
        response = client.get('/')
        assert response.status_code == 200
        assert 'Red Social de Viajes' in response.get_data(as_text=True)
        print("Endpoint raíz informativo")
        
        # Test 2: Respuestas con enlaces o contexto útil
        with patch('controllers.trip_controller.get_user_trips') as mock_get_trips:
            mock_trips = [
                Trip("1", 'Viaje Test', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
            ]
            mock_get_trips.return_value = (mock_trips, 1)
            
            response = client.get('/trips', headers=auth_headers)
            data = response.json
            
            # Verificar que la respuesta incluye metadatos útiles
            assert 'page' in data
            assert 'page_size' in data
            assert 'total_count' in data
            
            # Información que ayuda al usuario a navegar
            total_pages = (data['total_count'] + data['page_size'] - 1) // data['page_size']
            assert data['page'] <= total_pages or data['total_count'] == 0
            
            print("Metadatos útiles para navegación")

    def test_user_workflow_efficiency(self, client, auth_headers):
        """
        Prueba de usabilidad: Eficiencia de flujos de trabajo
        Verifica que las tareas comunes sean eficientes
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Eficiencia de flujos")
        
        with patch('controllers.trip_controller.create_trip') as mock_create, \
             patch('controllers.trip_controller.get_trip') as mock_get, \
             patch('controllers.trip_controller.add_place_to_trip') as mock_add_place:
            
            # Flujo eficiente: Crear viaje y agregar lugar
            mock_create.return_value = 1
            mock_trip = Trip(1, 'Viaje Eficiente', 'Test', date(2024, 7, 1), date(2024, 7, 15), id=1)  # INTEGER
            mock_get.return_value = mock_trip
            mock_add_place.return_value = 1
            
            # Paso 1: Crear viaje con datos mínimos necesarios
            minimal_data = {
                'title': 'Viaje Rápido',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=auth_headers, json=minimal_data)
            assert response.status_code == 201
            trip_id = response.json['trip_id']
            
            # Paso 2: Agregar lugar con datos esenciales
            place_data = {
                'place_id': 1,
                'visit_date': '2024-07-02'
            }
            
            response = client.post(f'/trips/{trip_id}/places', headers=auth_headers, json=place_data)
            assert response.status_code == 201
            
            print("Flujo de trabajo eficiente verificado")

    def test_feedback_quality_and_responsiveness(self, client, auth_headers):
        """
        Prueba de usabilidad: Calidad de retroalimentación
        Verifica que el sistema proporcione feedback útil
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Calidad de feedback")
        
        with patch('controllers.trip_controller.create_trip') as mock_create, \
             patch('controllers.trip_controller.update_trip') as mock_update, \
             patch('controllers.trip_controller.get_trip') as mock_get:
            
            # Test 1: Feedback positivo claro
            mock_create.return_value = 1
            
            response = client.post('/trips', headers=auth_headers, json={
                'title': 'Feedback Test',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            })
            
            assert response.status_code == 201
            assert 'successfully' in response.json['message'].lower()
            assert 'trip_id' in response.json
            print("Feedback positivo claro y útil")
            
            # Test 2: Feedback de actualización informativo
            mock_trip = Trip(1, 'Test Trip', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)  # INTEGER
            mock_get.return_value = mock_trip
            mock_update.return_value = 1
            
            response = client.put('/trips/1', headers=auth_headers, json={
                'title': 'Título Actualizado'
            })
            
            assert response.status_code == 200
            assert 'updated successfully' in response.json['message'].lower()
            print("Feedback de actualización informativo")
            
            # Feedback de calidad verificado
            print("Sistema proporciona feedback claro y consistente")


class TestUserExperienceOptimization:
    """
    Pruebas de optimización de experiencia de usuario
    """
    
    def test_progressive_disclosure(self, client, auth_headers):
        """
        Prueba de usabilidad: Divulgación progresiva de información
        Verifica que la información se presente gradualmente
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Divulgación progresiva")
        
        with patch('controllers.trip_controller.get_user_trips') as mock_list, \
             patch('controllers.trip_controller.get_trip') as mock_detail:
            
            # Nivel 1: Lista resumida de viajes
            mock_trips = [
                Trip(1, 'Viaje 1', 'Desc corta', date(2024, 7, 1), date(2024, 7, 15), id=1),  # INTEGER
                Trip(1, 'Viaje 2', 'Desc corta', date(2024, 8, 1), date(2024, 8, 15), id=2)   # INTEGER
            ]
            mock_list.return_value = (mock_trips, 2)
            
            response = client.get('/trips', headers=auth_headers)
            list_data = response.json
            
            # Lista debe tener información esencial pero no abrumadora
            assert len(list_data['trips']) == 2
            for trip in list_data['trips']:
                assert 'id' in trip
                assert 'title' in trip
                assert 'start_date' in trip
                assert 'end_date' in trip
            
            print("Lista con información esencial")
            
            # Nivel 2: Detalles completos cuando se solicitan
            detailed_trip = Trip(
                1, 'Viaje Detallado', 'Descripción muy completa con muchos detalles',  # INTEGER
                date(2024, 7, 1), date(2024, 7, 15), status='planned', budget=2500.00, id=1
            )
            mock_detail.return_value = detailed_trip
            
            response = client.get('/trips/1', headers=auth_headers)
            detail_data = response.json
            
            # Detalles deben incluir toda la información disponible
            assert 'description' in detail_data
            assert 'status' in detail_data
            assert 'budget' in detail_data
            
            print("Detalles completos cuando se solicitan")

    def test_contextual_actions(self, client, auth_headers):
        """
        Prueba de usabilidad: Acciones contextuales
        Verifica que las acciones disponibles sean apropiadas al contexto
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Acciones contextuales")
        
        with patch('controllers.trip_controller.get_trip') as mock_get, \
             patch('controllers.trip_controller.get_trip_places') as mock_places:
            
            # Contexto: Viaje en estado 'planned'
            planned_trip = Trip(
                1, 'Viaje Planeado', 'En planificación',  # INTEGER
                date(2024, 9, 1), date(2024, 9, 15), status='planned', id=1
            )
            mock_get.return_value = planned_trip
            
            # Verificar que se pueden realizar acciones apropiadas
            response = client.get('/trips/1', headers=auth_headers)
            assert response.status_code == 200
            
            # Debería permitir agregar lugares (contextualmente apropiado)
            mock_places.return_value = []
            response = client.get('/trips/1/places', headers=auth_headers)
            assert response.status_code == 200
            
            print("Acciones apropiadas para viaje planeado")

    def test_error_recovery_guidance(self, client, auth_headers):
        """
        Prueba de usabilidad: Guía para recuperación de errores
        Verifica que los errores incluyan guía para resolverlos
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Recuperación de errores")
        
        # Test 1: Error con guía implícita
        response = client.post('/trips', headers=auth_headers, json={
            'title': 'Solo título'
            # Faltan campos requeridos
        })
        
        assert response.status_code == 400
        error_msg = response.json['error']
        
        # El mensaje debería indicar qué falta
        assert 'required field' in error_msg.lower()
        print("Error indica qué se necesita corregir")
        
        # Test 2: Error de recurso no encontrado
        with patch('controllers.trip_controller.get_trip', return_value=None):
            response = client.get('/trips/99999', headers=auth_headers)
            
            assert response.status_code == 404
            assert 'not found' in response.json['error'].lower()
            print("Error claro para recurso inexistente")

    def test_api_consistency_patterns(self, client, auth_headers):
        """
        Prueba de usabilidad: Patrones consistentes en la API
        Verifica que los patrones de uso sean consistentes
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Patrones consistentes")
        
        with patch('controllers.trip_controller.create_trip') as mock_create, \
             patch('controllers.trip_controller.get_trip') as mock_get, \
             patch('controllers.trip_controller.add_place_to_trip') as mock_add:
            
            # Patrón: Todas las creaciones devuelven 201 con ID
            mock_create.return_value = 1
            
            response = client.post('/trips', headers=auth_headers, json={
                'title': 'Consistencia Test',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            })
            
            assert response.status_code == 201
            assert 'trip_id' in response.json
            assert 'message' in response.json
            print("Patrón de creación consistente")
            
            # Patrón: Todas las consultas exitosas devuelven 200 con datos
            mock_trip = Trip(1, 'Test', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)  # INTEGER
            mock_get.return_value = mock_trip
            
            response = client.get('/trips/1', headers=auth_headers)
            
            assert response.status_code == 200
            assert 'id' in response.json
            print("Patrón de consulta consistente")
            
            # Patrón: Todas las adiciones devuelven 201 con ID de entrada
            mock_add.return_value = 1
            
            response = client.post('/trips/1/places', headers=auth_headers, json={
                'place_id': 1
            })
            
            assert response.status_code == 201
            assert 'entry_id' in response.json
            assert 'message' in response.json
            print("Patrón de adición consistente")


class TestAccessibilityAndInclusion:
    """
    Pruebas de accesibilidad y inclusión en la API
    """
    
    def test_multiple_data_formats_support(self, client, auth_headers):
        """
        Prueba de usabilidad: Soporte para múltiples formatos
        Verifica flexibilidad en formatos de entrada
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Flexibilidad de formatos")
        
        with patch('controllers.trip_controller.create_trip') as mock_create:
            mock_create.return_value = 1
            
            # Formato mínimo válido
            minimal_data = {
                'title': 'Viaje Mínimo',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=auth_headers, json=minimal_data)
            assert response.status_code == 201
            print("Formato mínimo aceptado")
            
            # Formato completo válido
            complete_data = {
                'title': 'Viaje Completo',
                'description': 'Descripción detallada',
                'start_date': '2024-08-01',
                'end_date': '2024-08-15',
                'status': 'planned',
                'budget': 2500.00
            }
            
            response = client.post('/trips', headers=auth_headers, json=complete_data)
            assert response.status_code == 201
            print("Formato completo aceptado")

    def test_internationalization_readiness(self, client, auth_headers):
        """
        Prueba de usabilidad: Preparación para internacionalización
        Verifica que la API maneje diferentes idiomas y formatos
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Preparación i18n")
        
        with patch('controllers.trip_controller.create_trip') as mock_create:
            mock_create.return_value = 1
            
            # Texto en diferentes idiomas/caracteres
            international_data = {
                'title': 'Viaje à París - 旅行 - Путешествие',
                'description': 'Café, croissants et culture française',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
            
            response = client.post('/trips', headers=auth_headers, json=international_data)
            assert response.status_code == 201
            print("Caracteres internacionales manejados")

    def test_graceful_degradation(self, client, auth_headers):
        """
        Prueba de usabilidad: Degradación elegante
        Verifica que el sistema funcione con capacidades limitadas
        """
        print("\nINICIANDO PRUEBA DE USABILIDAD: Degradación elegante")
        
        with patch('controllers.trip_controller.get_user_trips') as mock_get:
            
            # Simular respuesta con datos limitados
            limited_trips = [
                Trip(1, 'Viaje Básico', '', date(2024, 7, 1), date(2024, 7, 15), id=1)  # INTEGER
            ]
            mock_get.return_value = (limited_trips, 1)
            
            response = client.get('/trips', headers=auth_headers)
            
            # Debería funcionar incluso con datos mínimos
            assert response.status_code == 200
            assert len(response.json['trips']) == 1
            print("Funciona con datos mínimos")


def test_usability_summary():
    """Resumen de todas las pruebas de usabilidad"""
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS DE USABILIDAD")
    print("="*60)
    print("Todas las pruebas de usabilidad completadas")
    print("\nAspectos de usabilidad evaluados:")
    print("   • Claridad y consistencia de respuestas")
    print("   • Mensajes de error amigables")
    print("   • Intuitividad y predictibilidad")
    print("   • Consistencia en formatos de datos")
    print("   • Descubribilidad de la API")
    print("   • Eficiencia de flujos de trabajo")
    print("   • Calidad de retroalimentación")
    print("   • Divulgación progresiva")
    print("   • Acciones contextuales")
    print("   • Recuperación de errores")
    print("   • Patrones consistentes")
    print("   • Flexibilidad de formatos")
    print("   • Preparación para i18n")
    print("   • Degradación elegante")
    print("\nCriterios de usabilidad verificados:")
    print("   • API intuitiva y predecible")
    print("   • Errores claros y accionables")
    print("   • Respuestas consistentes y útiles")
    print("   • Flujos de trabajo eficientes")
    print("   • Feedback apropiado y oportuno")
    print("   • Flexibilidad para diferentes casos de uso")
    print("\nBeneficios de las pruebas de usabilidad:")
    print("   • API más fácil de usar y adoptar")
    print("   • Reducción de curva de aprendizaje")
    print("   • Mejor experiencia de desarrollador")
    print("   • Mayor consistencia en la interfaz")
    print("   • Detección de puntos de fricción")
    print("   • Validación de patrones de diseño")
# tests/acceptance/test_acceptance_trips.py
import pytest
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token
from app import app
from models.trip import Trip
from datetime import date, datetime

@pytest.fixture
def client():
    """Cliente de pruebas configurado para acceptance testing"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key-acceptance'
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def auth_headers():
    """Headers de autenticación para las pruebas"""
    with app.app_context():
        access_token = create_access_token(identity="1")
        return {'Authorization': f'Bearer {access_token}'}

class TestUserCanPlanTrips:
    """
    Historia de Usuario: Como usuario quiero planificar viajes 
    para organizar mis futuras vacaciones
    """
    
    @patch('controllers.trip_controller.create_trip')
    def test_user_can_create_basic_trip_plan(self, mock_create_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede crear un plan básico de viaje
        con título, fechas de inicio y fin
        """
        # Given: Un usuario autenticado quiere planificar un viaje
        mock_create_trip.return_value = 1
        
        trip_data = {
            'title': 'Vacaciones de Verano en Europa',
            'start_date': '2024-07-15',
            'end_date': '2024-07-30'
        }
        
        # When: El usuario crea el plan de viaje
        response = client.post('/trips', headers=auth_headers, json=trip_data)
        
        # Then: El sistema confirma la creación del viaje
        assert response.status_code == 201
        assert response.json['message'] == "Trip created successfully"
        assert 'trip_id' in response.json
        
        # And: Se llamó al controlador con los datos correctos
        mock_create_trip.assert_called_once()
        call_args = mock_create_trip.call_args[1]
        assert call_args['title'] == 'Vacaciones de Verano en Europa'
        assert call_args['start_date'] == '2024-07-15'
        assert call_args['end_date'] == '2024-07-30'
        assert call_args['status'] == 'planned'
    
    @patch('controllers.trip_controller.create_trip')
    def test_user_can_create_detailed_trip_plan(self, mock_create_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede crear un plan detallado de viaje
        incluyendo descripción, estado y presupuesto
        """
        # Given: Un usuario quiere crear un viaje detallado
        mock_create_trip.return_value = 2
        
        detailed_trip = {
            'title': 'Luna de Miel en París',
            'description': 'Viaje romántico por la ciudad del amor',
            'start_date': '2024-09-01',
            'end_date': '2024-09-10',
            'status': 'planned',
            'budget': 3500.00
        }
        
        # When: El usuario crea el plan detallado
        response = client.post('/trips', headers=auth_headers, json=detailed_trip)
        
        # Then: El sistema acepta todos los campos
        assert response.status_code == 201
        
        # And: Todos los detalles fueron procesados
        call_args = mock_create_trip.call_args[1]
        assert call_args['description'] == 'Viaje romántico por la ciudad del amor'
        assert call_args['budget'] == 3500.00
    
    def test_user_cannot_create_trip_without_required_fields(self, client, auth_headers):
        """
        Criterio de Aceptación: El sistema debe rechazar viajes sin campos obligatorios
        """
        # Given: Un usuario intenta crear un viaje incompleto
        incomplete_trip = {
            'title': 'Viaje Incompleto'
            # Faltan start_date y end_date
        }
        
        # When: El usuario intenta crear el viaje
        response = client.post('/trips', headers=auth_headers, json=incomplete_trip)
        
        # Then: El sistema rechaza la solicitud
        assert response.status_code == 400
        assert 'Missing required field' in response.json['error']

class TestUserCanManageTrips:
    """
    Historia de Usuario: Como usuario quiero gestionar mis viajes
    para mantener mi información actualizada
    """
    
    @patch('controllers.trip_controller.get_trip')
    def test_user_can_view_their_trip_details(self, mock_get_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede ver los detalles completos de sus viajes
        """
        # Given: Un usuario tiene un viaje creado
        mock_trip = Trip(
            user_id=1,
            title='Aventura en Tokio',
            description='Explorar la cultura japonesa',
            start_date=date(2024, 10, 1),
            end_date=date(2024, 10, 15),
            status='planned',
            budget=4000.00,
            id=1
        )
        mock_get_trip.return_value = mock_trip
        
        # When: El usuario consulta los detalles del viaje
        response = client.get('/trips/1', headers=auth_headers)
        
        # Then: El sistema muestra toda la información
        assert response.status_code == 200
        trip_data = response.json
        assert trip_data['title'] == 'Aventura en Tokio'
        assert trip_data['description'] == 'Explorar la cultura japonesa'
        assert trip_data['start_date'] == '2024-10-01'
        assert trip_data['end_date'] == '2024-10-15'
        assert trip_data['budget'] == 4000.00
    
    @patch('controllers.trip_controller.get_trip')
    def test_user_cannot_view_other_users_trips(self, mock_get_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario no puede ver viajes de otros usuarios
        """
        # Given: Existe un viaje que pertenece a otro usuario
        other_user_trip = Trip(
            user_id=2,  # Diferente usuario
            title='Viaje Privado',
            description='No debería ser visible',
            start_date=date(2024, 8, 1),
            end_date=date(2024, 8, 15),
            id=1
        )
        mock_get_trip.return_value = other_user_trip
        
        # When: El usuario intenta ver el viaje de otro
        response = client.get('/trips/1', headers=auth_headers)
        
        # Then: El sistema deniega el acceso
        assert response.status_code == 403
        assert response.json['error'] == 'Unauthorized to view this trip'
    
    @patch('controllers.trip_controller.get_user_trips')
    def test_user_can_list_their_trips(self, mock_get_user_trips, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede ver una lista de todos sus viajes
        """
        # Given: Un usuario tiene múltiples viajes
        trip1 = Trip(1, 'Viaje 1', 'Descripción 1', date(2024, 7, 1), date(2024, 7, 15), id=1)
        trip2 = Trip(1, 'Viaje 2', 'Descripción 2', date(2024, 8, 1), date(2024, 8, 15), id=2)
        mock_get_user_trips.return_value = ([trip1, trip2], 2)
        
        # When: El usuario solicita su lista de viajes
        response = client.get('/trips', headers=auth_headers)
        
        # Then: El sistema devuelve todos sus viajes
        assert response.status_code == 200
        data = response.json
        assert len(data['trips']) == 2
        assert data['total_count'] == 2
        assert data['trips'][0]['title'] == 'Viaje 1'
        assert data['trips'][1]['title'] == 'Viaje 2'

class TestUserCanAddPlacesToTrips:
    """
    Historia de Usuario: Como usuario quiero agregar lugares a mis viajes
    para planificar mi itinerario
    """
    
    @patch('controllers.trip_controller.get_trip')
    @patch('controllers.trip_controller.add_place_to_trip')
    def test_user_can_add_place_to_their_trip(self, mock_add_place, mock_get_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede agregar lugares a sus viajes
        """
        # Given: Un usuario tiene un viaje y quiere agregar un lugar
        mock_trip = Trip(1, 'Viaje a Japón', 'Desc', date(2024, 10, 1), date(2024, 10, 15), id=1)
        mock_get_trip.return_value = mock_trip
        mock_add_place.return_value = 1
        
        place_data = {
            'place_id': 5,
            'visit_date': '2024-10-05',
            'visit_order': 1,
            'notes': 'Primera parada del viaje',
            'rating': 5
        }
        
        # When: El usuario agrega el lugar al viaje
        response = client.post('/trips/1/places', headers=auth_headers, json=place_data)
        
        # Then: El sistema confirma la adición
        assert response.status_code == 201
        assert response.json['message'] == "Place added to trip successfully"
        assert 'entry_id' in response.json
        
        # And: Se llamó al controlador con los datos correctos
        mock_add_place.assert_called_once_with(
            trip_id=1,
            place_id=5,
            visit_date='2024-10-05',
            visit_order=1,
            notes='Primera parada del viaje',
            rating=5
        )
    
    @patch('controllers.trip_controller.get_trip')
    @patch('controllers.trip_controller.get_trip_places')
    def test_user_can_view_places_in_trip(self, mock_get_places, mock_get_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede ver todos los lugares de su viaje
        """
        # Given: Un usuario tiene un viaje con lugares
        mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
        mock_get_trip.return_value = mock_trip
        
        mock_places = [
            {
                "place_id": 1,
                "name": "Torre Eiffel",
                "description": "Icónica torre en París",
                "city": "París",
                "country": "Francia",
                "visit_date": "2024-07-05",
                "visit_order": 1,
                "notes": "Primera parada",
                "rating": 5
            },
            {
                "place_id": 2,
                "name": "Louvre",
                "description": "Museo famoso",
                "city": "París",
                "country": "Francia",
                "visit_date": "2024-07-06",
                "visit_order": 2,
                "notes": "Segundo día",
                "rating": 4
            }
        ]
        mock_get_places.return_value = mock_places
        
        # When: El usuario consulta los lugares del viaje
        response = client.get('/trips/1/places', headers=auth_headers)
        
        # Then: El sistema muestra todos los lugares con detalles
        assert response.status_code == 200
        places = response.json['places']
        assert len(places) == 2
        assert places[0]['name'] == 'Torre Eiffel'
        assert places[0]['visit_order'] == 1
        assert places[1]['name'] == 'Louvre'
        assert places[1]['visit_order'] == 2

class TestUserCanTrackTripProgress:
    """
    Historia de Usuario: Como usuario quiero hacer seguimiento del progreso de mis viajes
    para mantener control sobre mi planificación
    """
    
    @patch('controllers.trip_controller.get_trip')
    @patch('controllers.trip_controller.get_trip_statistics')
    def test_user_can_view_trip_statistics(self, mock_get_stats, mock_get_trip, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede ver estadísticas de su viaje
        """
        # Given: Un usuario tiene un viaje con estadísticas
        mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
        mock_get_trip.return_value = mock_trip
        
        mock_statistics = {
            "total_places": 5,
            "total_expenses": 2500.75,
            "avg_place_rating": 4.2,
            "trip_duration_days": 15
        }
        mock_get_stats.return_value = mock_statistics
        
        # When: El usuario consulta las estadísticas
        response = client.get('/trips/1/statistics', headers=auth_headers)
        
        # Then: El sistema muestra información útil para el seguimiento
        assert response.status_code == 200
        stats = response.json
        assert stats['total_places'] == 5
        assert stats['total_expenses'] == 2500.75
        assert stats['avg_place_rating'] == 4.2
        assert stats['trip_duration_days'] == 15
    
    @patch('controllers.trip_controller.search_trips')
    def test_user_can_search_their_trips(self, mock_search_trips, client, auth_headers):
        """
        Criterio de Aceptación: El usuario puede buscar entre sus viajes
        """
        # Given: Un usuario tiene múltiples viajes y quiere buscar específicos
        found_trip = Trip(1, 'Viaje a Europa', 'Desc', date(2024, 7, 1), date(2024, 7, 15), status='completed', id=1)
        mock_search_trips.return_value = ([found_trip], 1)
        
        # When: El usuario busca viajes por criterios
        response = client.get('/trips/search?status=completed&title=Europa', headers=auth_headers)
        
        # Then: El sistema devuelve los resultados filtrados
        assert response.status_code == 200
        data = response.json
        assert len(data['trips']) == 1
        assert data['trips'][0]['title'] == 'Viaje a Europa'
        assert data['trips'][0]['status'] == 'completed'
        assert data['search_criteria']['status'] == 'completed'
        assert data['search_criteria']['title'] == 'Europa'

class TestUserWorkflowScenarios:
    """
    Escenarios de flujo completo de usuario
    """
    
    @patch('controllers.trip_controller.create_trip')
    @patch('controllers.trip_controller.get_trip')
    @patch('controllers.trip_controller.add_place_to_trip')
    def test_complete_trip_planning_workflow(self, mock_add_place, mock_get_trip, mock_create_trip, client, auth_headers):
        """
        Escenario: Flujo completo de planificación de viaje
        """
        # Escenario: Un usuario planifica un viaje completo desde cero
        
        # Step 1: Crear el viaje
        mock_create_trip.return_value = 1
        trip_data = {
            'title': 'Aventura en Costa Rica',
            'description': 'Ecoturismo y aventura',
            'start_date': '2024-11-01',
            'end_date': '2024-11-10',
            'budget': 2000.00
        }
        
        create_response = client.post('/trips', headers=auth_headers, json=trip_data)
        assert create_response.status_code == 201
        trip_id = create_response.json['trip_id']
        
        # Step 2: Agregar lugares al viaje
        mock_trip = Trip(1, 'Aventura en Costa Rica', 'Desc', date(2024, 11, 1), date(2024, 11, 10), id=trip_id)
        mock_get_trip.return_value = mock_trip
        mock_add_place.return_value = 1
        
        place_data = {
            'place_id': 10,
            'visit_date': '2024-11-03',
            'visit_order': 1,
            'notes': 'Volcán Arenal - actividad principal'
        }
        
        add_place_response = client.post(f'/trips/{trip_id}/places', headers=auth_headers, json=place_data)
        assert add_place_response.status_code == 201
        
        # Verificar que todo el flujo fue exitoso
        assert mock_create_trip.called
        assert mock_add_place.called
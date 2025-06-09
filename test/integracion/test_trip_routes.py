# tests/integracion/test_trip_routes.py
import pytest
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token
from app import app
from models.trip import Trip
from datetime import date

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('controllers.trip_controller.create_trip')
def test_create_trip_success(mock_create_trip, client):
    """Test de creación exitosa de un viaje"""
    mock_create_trip.return_value = 1
    
    access_token = create_access_token(identity=1)
    
    response = client.post(
        '/trips',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'title': 'Viaje a Europa',
            'description': 'Mi primer viaje internacional',
            'start_date': '2024-07-01',
            'end_date': '2024-07-15',
            'status': 'planned',
            'budget': 2500.00
        }
    )

    assert response.status_code == 201
    assert response.json == {"message": "Trip created successfully", "trip_id": 1}
    mock_create_trip.assert_called_once_with(
        user_id=1,
        title='Viaje a Europa',
        description='Mi primer viaje internacional',
        start_date='2024-07-01',
        end_date='2024-07-15',
        status='planned',
        budget=2500.00
    )

@patch('controllers.trip_controller.create_trip')
def test_create_trip_minimal_data(mock_create_trip, client):
    """Test de creación de viaje con datos mínimos"""
    mock_create_trip.return_value = 2
    
    access_token = create_access_token(identity=1)
    
    response = client.post(
        '/trips',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'title': 'Viaje Corto',
            'start_date': '2024-08-01',
            'end_date': '2024-08-03'
        }
    )

    assert response.status_code == 201
    assert response.json == {"message": "Trip created successfully", "trip_id": 2}

def test_create_trip_missing_required_fields(client):
    """Test de creación de viaje con campos faltantes"""
    access_token = create_access_token(identity=1)
    
    response = client.post(
        '/trips',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'title': 'Viaje Incompleto'
            # Falta start_date y end_date
        }
    )

    assert response.status_code == 400
    assert 'Missing required field' in response.json['error']

@patch('controllers.trip_controller.get_trip')
def test_get_trip_success(mock_get_trip, client):
    """Test de obtención exitosa de un viaje"""
    mock_trip = Trip(
        user_id=1,
        title='Viaje a Europa',
        description='Mi primer viaje internacional',
        start_date=date(2024, 7, 1),
        end_date=date(2024, 7, 15),
        status='planned',
        budget=2500.00,
        id=1
    )
    mock_get_trip.return_value = mock_trip
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json['title'] == 'Viaje a Europa'
    assert response.json['user_id'] == 1
    assert response.json['id'] == 1

@patch('controllers.trip_controller.get_trip')
def test_get_trip_unauthorized(mock_get_trip, client):
    """Test de obtención de viaje no autorizado"""
    mock_trip = Trip(
        user_id=2,  # Diferente usuario
        title='Viaje Privado',
        description='Viaje de otro usuario',
        start_date=date(2024, 7, 1),
        end_date=date(2024, 7, 15),
        id=1
    )
    mock_get_trip.return_value = mock_trip
    
    access_token = create_access_token(identity=1)  # Usuario 1 intenta ver viaje del usuario 2
    
    response = client.get(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 403
    assert response.json['error'] == 'Unauthorized to view this trip'

@patch('controllers.trip_controller.get_trip')
def test_get_trip_not_found(mock_get_trip, client):
    """Test de obtención de viaje que no existe"""
    mock_get_trip.return_value = None
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/999',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 404
    assert response.json['error'] == 'Trip not found'

@patch('controllers.trip_controller.get_user_trips')
def test_get_user_trips_success(mock_get_user_trips, client):
    """Test de obtención de viajes del usuario"""
    mock_trip1 = Trip(1, 'Viaje 1', 'Desc 1', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_trip2 = Trip(1, 'Viaje 2', 'Desc 2', date(2024, 8, 1), date(2024, 8, 10), id=2)
    
    mock_get_user_trips.return_value = ([mock_trip1, mock_trip2], 2)
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips?page=1&page_size=10',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json['trips']) == 2
    assert response.json['total_count'] == 2
    assert response.json['page'] == 1
    assert response.json['page_size'] == 10

@patch('controllers.trip_controller.get_user_trips')
def test_get_user_trips_with_status_filter(mock_get_user_trips, client):
    """Test de obtención de viajes filtrados por estado"""
    mock_trip = Trip(1, 'Viaje Completado', 'Desc', date(2024, 7, 1), date(2024, 7, 15), status='completed', id=1)
    mock_get_user_trips.return_value = ([mock_trip], 1)
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips?status=completed',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json['trips']) == 1
    assert response.json['trips'][0]['status'] == 'completed'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.update_trip')
def test_update_trip_success(mock_update_trip, mock_get_trip, client):
    """Test de actualización exitosa de un viaje"""
    mock_trip = Trip(1, 'Viaje Original', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_update_trip.return_value = 1
    
    access_token = create_access_token(identity=1)
    
    response = client.put(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'title': 'Viaje Actualizado',
            'description': 'Nueva descripción',
            'status': 'in_progress'
        }
    )

    assert response.status_code == 200
    assert response.json == {"message": "Trip updated successfully", "trip_id": 1}

@patch('controllers.trip_controller.get_trip')
def test_update_trip_unauthorized(mock_get_trip, client):
    """Test de actualización no autorizada"""
    mock_trip = Trip(2, 'Viaje de Otro', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    
    access_token = create_access_token(identity=1)
    
    response = client.put(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'title': 'Intento de Hack'}
    )

    assert response.status_code == 403
    assert response.json['error'] == 'Unauthorized or trip not found'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.delete_trip')
def test_delete_trip_success(mock_delete_trip, mock_get_trip, client):
    """Test de eliminación exitosa de un viaje"""
    mock_trip = Trip(1, 'Viaje a Eliminar', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_delete_trip.return_value = 1
    
    access_token = create_access_token(identity=1)
    
    response = client.delete(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json == {"message": "Trip deleted successfully", "trip_id": 1}

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.add_place_to_trip')
def test_add_place_to_trip_success(mock_add_place, mock_get_trip, client):
    """Test de agregar lugar a viaje exitosamente"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_add_place.return_value = 1
    
    access_token = create_access_token(identity=1)
    
    response = client.post(
        '/trips/1/places',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'place_id': 5,
            'visit_date': '2024-07-05',
            'visit_order': 1,
            'notes': 'Primera parada',
            'rating': 5
        }
    )

    assert response.status_code == 201
    assert response.json == {"message": "Place added to trip successfully", "entry_id": 1}

def test_add_place_to_trip_missing_place_id(client):
    """Test de agregar lugar sin place_id"""
    access_token = create_access_token(identity=1)
    
    response = client.post(
        '/trips/1/places',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'notes': 'Sin place_id'}
    )

    assert response.status_code == 400
    assert response.json['error'] == 'Missing required field: place_id'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.remove_place_from_trip')
def test_remove_place_from_trip_success(mock_remove_place, mock_get_trip, client):
    """Test de eliminar lugar de viaje exitosamente"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_remove_place.return_value = 1
    
    access_token = create_access_token(identity=1)
    
    response = client.delete(
        '/trips/1/places/5',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json == {"message": "Place removed from trip successfully", "entry_id": 1}

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.remove_place_from_trip')
def test_remove_place_from_trip_not_found(mock_remove_place, mock_get_trip, client):
    """Test de eliminar lugar que no está en el viaje"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_remove_place.return_value = None
    
    access_token = create_access_token(identity=1)
    
    response = client.delete(
        '/trips/1/places/999',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 404
    assert response.json['error'] == 'Place not found in trip'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.get_trip_places')
def test_get_trip_places_success(mock_get_trip_places, mock_get_trip, client):
    """Test de obtener lugares de un viaje"""
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
    mock_get_trip_places.return_value = mock_places
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/1/places',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json['places']) == 2
    assert response.json['places'][0]['name'] == 'Torre Eiffel'
    assert response.json['places'][1]['name'] == 'Louvre'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.get_trip_statistics')
def test_get_trip_statistics_success(mock_get_statistics, mock_get_trip, client):
    """Test de obtener estadísticas de un viaje"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    
    mock_statistics = {
        "total_places": 3,
        "total_expenses": 1500.50,
        "avg_place_rating": 4.33,
        "trip_duration_days": 15
    }
    mock_get_statistics.return_value = mock_statistics
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/1/statistics',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert response.json['total_places'] == 3
    assert response.json['total_expenses'] == 1500.50
    assert response.json['avg_place_rating'] == 4.33
    assert response.json['trip_duration_days'] == 15

@patch('controllers.trip_controller.search_trips')
def test_search_trips_success(mock_search_trips, client):
    """Test de búsqueda de viajes"""
    mock_trip = Trip(1, 'Viaje Europa', 'Desc', date(2024, 7, 1), date(2024, 7, 15), status='completed', id=1)
    mock_search_trips.return_value = ([mock_trip], 1)
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/search?status=completed&title=Europa&page=1&page_size=5',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json['trips']) == 1
    assert response.json['total_count'] == 1
    assert response.json['trips'][0]['title'] == 'Viaje Europa'
    assert response.json['search_criteria']['status'] == 'completed'
    assert response.json['search_criteria']['title'] == 'Europa'

@patch('controllers.trip_controller.search_trips')
def test_search_trips_no_results(mock_search_trips, client):
    """Test de búsqueda sin resultados"""
    mock_search_trips.return_value = ([], 0)
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/search?title=NoExiste',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    assert len(response.json['trips']) == 0
    assert response.json['total_count'] == 0

def test_unauthorized_request(client):
    """Test de request sin token de autorización"""
    response = client.get('/trips')
    
    # CORREGIDO: Tu aplicación devuelve 401
    assert response.status_code == 401  # Cambiado de 422 a 401

def test_create_trip_with_exception(client):
    """Test de manejo de excepción en creación de viaje"""
    access_token = create_access_token(identity=1)
    
    with patch('controllers.trip_controller.create_trip', side_effect=Exception('Database error')):
        response = client.post(
            '/trips',
            headers={'Authorization': f'Bearer {access_token}'},
            json={
                'title': 'Viaje con Error',
                'start_date': '2024-07-01',
                'end_date': '2024-07-15'
            }
        )

    assert response.status_code == 400
    assert 'Database error' in response.json['error']

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.update_trip')
def test_update_trip_failed(mock_update_trip, mock_get_trip, client):
    """Test de falla en actualización de viaje"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_update_trip.return_value = None
    
    access_token = create_access_token(identity=1)
    
    response = client.put(
        '/trips/1',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'title': 'Nuevo Título'}
    )

    assert response.status_code == 400
    assert response.json['error'] == 'Failed to update trip'

@patch('controllers.trip_controller.get_trip')
@patch('controllers.trip_controller.get_trip_statistics')
def test_get_trip_statistics_failed(mock_get_statistics, mock_get_trip, client):
    """Test de falla en obtener estadísticas"""
    mock_trip = Trip(1, 'Viaje', 'Desc', date(2024, 7, 1), date(2024, 7, 15), id=1)
    mock_get_trip.return_value = mock_trip
    mock_get_statistics.return_value = None
    
    access_token = create_access_token(identity=1)
    
    response = client.get(
        '/trips/1/statistics',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 400
    assert response.json['error'] == 'Failed to get trip statistics'
# tests/unitarias/test_trip_controller.py
import pytest
from controllers import trip_controller
from models.trip import Trip
from datetime import date

def test_create_trip(mocker):
    """Test de creación de un viaje exitosa"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    trip_id = trip_controller.create_trip(
        user_id=1,
        title="Viaje a Europa",
        description="Mi primer viaje internacional",
        start_date="2024-07-01",
        end_date="2024-07-15",
        status="planned",
        budget=2500.00
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_trip(%s, %s, %s, %s, %s, %s, %s)",
        (1, "Viaje a Europa", "Mi primer viaje internacional", "2024-07-01", "2024-07-15", "planned", 2500.00)
    )
    assert trip_id == 1

def test_create_trip_without_budget(mocker):
    """Test de creación de viaje sin presupuesto"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [2]

    trip_id = trip_controller.create_trip(
        user_id=2,
        title="Viaje local",
        description="Escapada de fin de semana",
        start_date="2024-08-01",
        end_date="2024-08-03"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_trip(%s, %s, %s, %s, %s, %s, %s)",
        (2, "Viaje local", "Escapada de fin de semana", "2024-08-01", "2024-08-03", "planned", None)
    )
    assert trip_id == 2

def test_get_trip_success(mocker):
    """Test de obtención exitosa de un viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Datos simulados de retorno de la BD
    mock_cursor.fetchone.return_value = (
        1, 1, "Viaje a Europa", "Mi primer viaje internacional", 
        date(2024, 7, 1), date(2024, 7, 15), "planned", 2500.00
    )

    trip = trip_controller.get_trip(trip_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_trip_by_id(%s)", (1,)
    )
    
    assert isinstance(trip, Trip)
    assert trip.id == 1
    assert trip.user_id == 1
    assert trip.title == "Viaje a Europa"
    assert trip.description == "Mi primer viaje internacional"
    assert trip.start_date == date(2024, 7, 1)
    assert trip.end_date == date(2024, 7, 15)
    assert trip.status == "planned"
    assert trip.budget == 2500.00

def test_get_trip_not_found(mocker):
    """Test cuando el viaje no existe"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    trip = trip_controller.get_trip(trip_id=999)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_trip_by_id(%s)", (999,)
    )
    assert trip is None

def test_get_user_trips_with_data(mocker):
    """Test de obtención de viajes de un usuario con datos"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Simulando dos viajes con total_count
    mock_cursor.fetchall.return_value = [
        (1, 1, "Viaje 1", "Descripción 1", date(2024, 7, 1), date(2024, 7, 15), "completed", 2000.00, None, None, 2),
        (2, 1, "Viaje 2", "Descripción 2", date(2024, 8, 1), date(2024, 8, 10), "planned", 1500.00, None, None, 2)
    ]

    trips, total_count = trip_controller.get_user_trips(user_id=1, page=1, page_size=10)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_user_trips(%s, %s, %s, %s)", (1, None, 1, 10)
    )
    
    assert len(trips) == 2
    assert total_count == 2
    assert isinstance(trips[0], Trip)
    assert trips[0].title == "Viaje 1"
    assert trips[1].title == "Viaje 2"

def test_get_user_trips_with_status_filter(mocker):
    """Test de obtención de viajes filtrados por estado"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, 1, "Viaje Completado", "Descripción", date(2024, 7, 1), date(2024, 7, 15), "completed", 2000.00, None, None, 1)
    ]

    trips, total_count = trip_controller.get_user_trips(user_id=1, status="completed", page=1, page_size=10)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_user_trips(%s, %s, %s, %s)", (1, "completed", 1, 10)
    )
    
    assert len(trips) == 1
    assert total_count == 1
    assert trips[0].status == "completed"

def test_get_user_trips_empty(mocker):
    """Test cuando el usuario no tiene viajes"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    trips, total_count = trip_controller.get_user_trips(user_id=999)

    assert trips == []
    assert total_count == 0

def test_update_trip_success(mocker):
    """Test de actualización exitosa de un viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    updated_trip_id = trip_controller.update_trip(
        trip_id=1,
        title="Viaje Actualizado",
        description="Descripción actualizada",
        start_date="2024-07-05",
        end_date="2024-07-20",
        status="in_progress",
        budget=3000.00
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT update_trip(%s, %s, %s, %s, %s, %s, %s)",
        (1, "Viaje Actualizado", "Descripción actualizada", "2024-07-05", "2024-07-20", "in_progress", 3000.00)
    )
    assert updated_trip_id == 1

def test_update_trip_not_found(mocker):
    """Test de actualización de viaje que no existe"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    updated_trip_id = trip_controller.update_trip(
        trip_id=999,
        title="Viaje No Existe",
        description="Descripción",
        start_date="2024-07-01",
        end_date="2024-07-15",
        status="planned",
        budget=1000.00
    )

    assert updated_trip_id is None

def test_delete_trip_success(mocker):
    """Test de eliminación exitosa de un viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    deleted_trip_id = trip_controller.delete_trip(trip_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT delete_trip(%s)", (1,)
    )
    assert deleted_trip_id == 1

def test_delete_trip_not_found(mocker):
    """Test de eliminación de viaje que no existe"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    deleted_trip_id = trip_controller.delete_trip(trip_id=999)

    assert deleted_trip_id is None

def test_add_place_to_trip_success(mocker):
    """Test de agregar lugar a viaje exitosamente"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    entry_id = trip_controller.add_place_to_trip(
        trip_id=1,
        place_id=5,
        visit_date="2024-07-05",
        visit_order=1,
        notes="Primera parada del viaje",
        rating=5
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_place_to_trip(%s, %s, %s, %s, %s, %s)",
        (1, 5, "2024-07-05", 1, "Primera parada del viaje", 5)
    )
    assert entry_id == 1

def test_add_place_to_trip_minimal_data(mocker):
    """Test de agregar lugar con datos mínimos"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [2]

    entry_id = trip_controller.add_place_to_trip(
        trip_id=1,
        place_id=3
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_place_to_trip(%s, %s, %s, %s, %s, %s)",
        (1, 3, None, None, None, None)
    )
    assert entry_id == 2

def test_remove_place_from_trip_success(mocker):
    """Test de eliminar lugar de viaje exitosamente"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    deleted_entry_id = trip_controller.remove_place_from_trip(trip_id=1, place_id=5)

    mock_cursor.execute.assert_called_once_with(
        "SELECT remove_place_from_trip(%s, %s)", (1, 5)
    )
    assert deleted_entry_id == 1

def test_remove_place_from_trip_not_found(mocker):
    """Test de eliminar lugar que no está en el viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    deleted_entry_id = trip_controller.remove_place_from_trip(trip_id=1, place_id=999)

    assert deleted_entry_id is None

def test_get_trip_places_success(mocker):
    """Test de obtener lugares de un viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Torre Eiffel", "Icónica torre en París", "París", "Francia", date(2024, 7, 5), 1, "Primera parada", 5),
        (2, "Louvre", "Museo famoso", "París", "Francia", date(2024, 7, 6), 2, "Segundo día", 4)
    ]

    places = trip_controller.get_trip_places(trip_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_trip_places(%s)", (1,)
    )
    
    assert len(places) == 2
    assert places[0]["name"] == "Torre Eiffel"
    assert places[0]["visit_order"] == 1
    assert places[0]["rating"] == 5
    assert places[1]["name"] == "Louvre"
    assert places[1]["visit_order"] == 2

def test_get_trip_places_empty(mocker):
    """Test de obtener lugares cuando el viaje no tiene lugares"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    places = trip_controller.get_trip_places(trip_id=1)

    assert places == []

def test_get_trip_statistics_success(mocker):
    """Test de obtener estadísticas de un viaje"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # total_places, total_expenses, avg_rating, duration_days
    mock_cursor.fetchone.return_value = (3, 1500.50, 4.33, 15)

    statistics = trip_controller.get_trip_statistics(trip_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_trip_statistics(%s)", (1,)
    )
    
    assert statistics["total_places"] == 3
    assert statistics["total_expenses"] == 1500.50
    assert statistics["avg_place_rating"] == 4.33
    assert statistics["trip_duration_days"] == 15

def test_get_trip_statistics_no_data(mocker):
    """Test de estadísticas cuando no hay datos"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    statistics = trip_controller.get_trip_statistics(trip_id=999)

    assert statistics is None

def test_search_trips_by_user_simplified(mocker):
    """Test simplificado de búsqueda de viajes por usuario"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Simular que no hay resultados (caso válido)
    mock_cursor.fetchall.return_value = []

    trips, total_count = trip_controller.search_trips(user_id=999, page=1, page_size=10)

    # Verificar que la función se ejecutó correctamente
    assert mock_cursor.execute.called
    assert trips == []
    assert total_count == 0

def test_search_trips_with_filters(mocker):
    """Test de búsqueda con múltiples filtros"""
    mock_conn = mocker.patch('controllers.trip_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = []

    trips, total_count = trip_controller.search_trips(
        user_id=1,
        status="completed",
        start_date_from="2024-01-01",
        start_date_to="2024-12-31",
        title_search="Europa",
        page=1,
        page_size=5
    )

    # Verificar que se ejecutó la consulta con los filtros
    assert mock_cursor.execute.called
    assert trips == []
    assert total_count == 0
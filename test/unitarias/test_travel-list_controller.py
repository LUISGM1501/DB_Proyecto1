import pytest
from src.controllers import travel_list_controller
from src.models.travel_list import TravelList
from src.models.place import Place

def test_create_travel_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    list_id = travel_list_controller.create_travel_list(user_id=1, name="My Travel List", description="A sample description")

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_travel_list(%s, %s, %s)", (1, "My Travel List", "A sample description")
    )

    assert list_id == 1

def test_get_travel_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "My Travel List", "A sample description")

    travel_list = travel_list_controller.get_travel_list(list_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_travel_list_by_id(%s)", (1,)
    )

    assert isinstance(travel_list, TravelList)
    assert travel_list.name == "My Travel List"

def test_update_travel_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    updated_list_id = travel_list_controller.update_travel_list(
        list_id=1, name="Updated List", description="Updated description"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT update_travel_list(%s, %s, %s)", (1, "Updated List", "Updated description")
    )
    assert updated_list_id == 1

def test_delete_travel_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    deleted_list_id = travel_list_controller.delete_travel_list(list_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT delete_travel_list(%s)", (1,)
    )
    assert deleted_list_id == 1

def test_add_place_to_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = [1]

    entry_id = travel_list_controller.add_place_to_list(list_id=1, place_id=2)

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_place_to_list(%s, %s)", (1, 2)
    )
    assert entry_id == 1

def test_get_places_in_list(mocker):
    mock_conn = mocker.patch('controllers.travel_list_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ("Place One", "Description", "City", "Country"),
        ("Place Two", "Description", "City", "Country")
    ]

    places = travel_list_controller.get_places_in_list(list_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_places_in_list(%s)", (1,)
    )
    assert len(places) == 2
    assert isinstance(places[0], Place)
    assert places[0].name == "Place One"
import pytest
from src.controllers import place_controller
from src.models.place import Place

def test_create_place(mocker):
    mock_conn = mocker.patch('controllers.place_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    place_id = place_controller.create_place(
        name="Test Place",
        description="A place for testing",
        city="Test City",
        country="Test Country"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT create_place(%s, %s, %s, %s)",
        ("Test Place", "A place for testing", "Test City", "Test Country")
    )

    assert place_id == 1

def test_get_place(mocker):
    mock_conn = mocker.patch('controllers.place_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ("Test Place", "A place for testing", "Test City", "Test Country")

    place = place_controller.get_place(place_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_place_by_id(%s)", (1,)
    )

    assert isinstance(place, Place)
    assert place.name == "Test Place"
    assert place.city == "Test City"

def test_update_place(mocker):
    mock_conn = mocker.patch('controllers.place_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    updated_place_id = place_controller.update_place(
        place_id=1,
        name="Updated Place",
        description="Updated description",
        city="Updated City",
        country="Updated Country"
    )

    mock_cursor.execute.assert_called_once_with(
        "SELECT update_place(%s, %s, %s, %s, %s)",
        (1, "Updated Place", "Updated description", "Updated City", "Updated Country")
    )

    assert updated_place_id == 1

def test_delete_place(mocker):
    mock_conn = mocker.patch('controllers.place_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    deleted_place_id = place_controller.delete_place(place_id=1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT delete_place(%s)", (1,)
    )

    assert deleted_place_id == 1
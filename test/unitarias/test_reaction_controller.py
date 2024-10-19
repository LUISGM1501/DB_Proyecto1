import pytest
from controllers import reaction_controller

def test_add_or_update_reaction(mocker):
    mock_conn = mocker.patch('controllers.reaction_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [True]

    success = reaction_controller.add_or_update_reaction(user_id=1, post_id=123, reaction_type="like")

    mock_cursor.execute.assert_called_once_with(
        "SELECT add_or_update_reaction(%s, %s, %s)", (1, 123, "like")
    )
    
    assert success is True

def test_get_reaction_counts(mocker):
    mock_conn = mocker.patch('controllers.reaction_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ("like", 10),
        ("love", 5),
        ("wow", 2)
    ]

    counts = reaction_controller.get_reaction_counts(post_id=123)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM get_reaction_counts(%s)", (123,)
    )
    
    assert len(counts) == 3
    assert counts == [("like", 10), ("love", 5), ("wow", 2)]
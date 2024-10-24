import pytest
from src.controllers import search_controller

def test_search_content(mocker):
    mock_conn = mocker.patch('controllers.search_controller.get_postgres_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "post", "Sample Post", "This is a sample post description", "2024-10-14"),
        (2, "comment", "Sample Comment", "This is a sample comment description", "2024-10-14")
    ]

    results = search_controller.search_content(query="sample")

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM search_content(%s)", ("sample",)
    )

    assert len(results) == 2
    assert results == [
        {
            "id": 1,
            "content_type": "post",
            "title": "Sample Post",
            "description": "This is a sample post description",
            "created_at": "2024-10-14"
        },
        {
            "id": 2,
            "content_type": "comment",
            "title": "Sample Comment",
            "description": "This is a sample comment description",
            "created_at": "2024-10-14"
        }
    ]

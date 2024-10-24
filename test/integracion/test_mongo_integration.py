# tests/integration/test_mongo_integration.py
import pytest
from src.services.mongo_service import MongoService
from src.controllers.mongo_controller import MongoController

@pytest.fixture
def mongo_controller():
    return MongoController()

def test_create_travel_record_integration(mongo_controller):
    travel_data = {
        'title': 'Integration Test Travel',
        'description': 'Test Description',
        'places': [
            {'id': 1, 'name': 'Test Place', 'country': 'Test Country'}
        ]
    }
    
    result = mongo_controller.create_travel_record(user_id=1, travel_data=travel_data)
    
    assert result['status'] == 'success'
    assert 'travel_id' in result

def test_create_review_integration(mongo_controller):
    review_data = {
        'rating': 5,
        'text': 'Great place!',
        'visit_date': '2023-10-15',
        'recommendations': ['Great for families']
    }
    
    result = mongo_controller.create_detailed_review(
        user_id=1,
        place_id=1,
        review_data=review_data
    )
    
    assert result['status'] == 'success'
    assert 'review_id' in result

def test_get_user_activity_summary_integration(mongo_controller):
    result = mongo_controller.get_user_activity_summary(user_id=1)
    
    assert result['status'] == 'success'
    assert 'stats' in result
    assert 'recent_activities' in result
from datetime import datetime, UTC

class TravelList:
    def __init__(self, user_id, name, description, id=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.places = []
        self.followers = []

    # to_dict: Convierte el objeto TravelList a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "places": self.places,
            "followers": self.followers
        }

class TravelListPlace:
    def __init__(self, travel_list_id, place_id, id=None):
        self.id = id
        self.travel_list_id = travel_list_id
        self.place_id = place_id

    # to_dict: Convierte el objeto TravelListPlace a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "travel_list_id": self.travel_list_id,
            "place_id": self.place_id
        }

class TravelListFollower:
    def __init__(self, travel_list_id, user_id, id=None):
        self.id = id
        self.travel_list_id = travel_list_id
        self.user_id = user_id

    # to_dict: Convierte el objeto TravelListFollower a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "travel_list_id": self.travel_list_id,
            "user_id": self.user_id
        }
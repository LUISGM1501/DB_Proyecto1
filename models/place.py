from datetime import datetime, UTC

class Place:
    def __init__(self, name, description, city, country, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.city = city
        self.country = country
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.image_links = []
        self.comments = []
        self.likes = []

    # to_dict: Convierte el objeto Place a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "country": self.country,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "image_links": self.image_links,
            "comments": self.comments,
            "likes": self.likes
        }

class PlaceImageLink:
    def __init__(self, place_id, image_url, id=None):
        self.id = id
        self.place_id = place_id
        self.image_url = image_url

    # to_dict: Convierte el objeto PlaceImageLink a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "image_url": self.image_url
        }
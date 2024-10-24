from datetime import datetime
from zoneinfo import ZoneInfo

class Like:
    def __init__(self, user_id, post_id=None, place_id=None, id=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.place_id = place_id
        self.created_at = datetime.now(ZoneInfo("UTC"))

    # to_dict: Convierte el objeto Like a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "place_id": self.place_id,
            "created_at": self.created_at
        }
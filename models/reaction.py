from datetime import datetime
from zoneinfo import ZoneInfo

class Reaction:
    def __init__(self, user_id, post_id, reaction_type, id=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.reaction_type = reaction_type
        self.created_at = datetime.now(ZoneInfo("UTC"))

    # to_dict: Convierte el objeto Reaction a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "reaction_type": self.reaction_type,
            "created_at": self.created_at
        }
from datetime import datetime, UTC

class Comment:
    def __init__(self, user_id, content, post_id=None, place_id=None, id=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.post_id = post_id
        self.place_id = place_id
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    # to_dict: Convierte el objeto Comment a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "post_id": self.post_id,
            "place_id": self.place_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
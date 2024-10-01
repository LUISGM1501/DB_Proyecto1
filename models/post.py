from datetime import datetime, UTC

class Post:
    def __init__(self, user_id, content, id=None):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.media_links = []
        self.comments = []
        self.likes = []
        self.reactions = []

    # to_dict: Convierte el objeto Post a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "media_links": self.media_links,
            "comments": self.comments,
            "likes": self.likes,
            "reactions": self.reactions
        }

class PostMediaLink:
    def __init__(self, post_id, media_url, media_type, id=None):
        self.id = id
        self.post_id = post_id
        self.media_url = media_url
        self.media_type = media_type

    # to_dict: Convierte el objeto PostMediaLink a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "media_url": self.media_url,
            "media_type": self.media_type
        }
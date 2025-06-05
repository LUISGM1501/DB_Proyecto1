# models/user.py
from datetime import datetime
from zoneinfo import ZoneInfo

class User:
    def __init__(self, username, email, password, bio=None, profile_picture_url=None, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.profile_picture_url = profile_picture_url
        self.created_at = datetime.now(ZoneInfo("UTC"))
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    # to_dict: Convierte el objeto User a un diccionario
    # Lo que facilita la conversion a JSON
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "profile_picture_url": self.profile_picture_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
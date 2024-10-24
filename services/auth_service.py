from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from controllers import user_controller

def authenticate_user(username, password):
    user = user_controller.get_user_by_username(username)
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return access_token
    return None
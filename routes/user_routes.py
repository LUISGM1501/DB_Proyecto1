from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from services.auth_service import authenticate_user
from flask import Blueprint, request, jsonify
from controllers import user_controller

user_routes = Blueprint('user_routes', __name__)

# Crear un nuevo usuario
@user_routes.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json
    try:
        user_id = user_controller.create_user(
            data['username'],
            data['email'],
            data['password'],
            data.get('bio'),
            data.get('profile_picture_url')
        )
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un usuario por ID
@user_routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
# Login
@user_routes.route('/login', methods=['POST'])
@jwt_required()
def login():
    data = request.json
    access_token = authenticate_user(data['username'], data['password'])
    if access_token:
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Funcion para proteger las rutas
@user_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

@user_routes.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
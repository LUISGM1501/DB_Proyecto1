from flask import Blueprint, request, jsonify
from controllers import travel_list_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

travel_list_routes = Blueprint('travel_list_routes', __name__)

# Crear una nueva lista de viaje
@travel_list_routes.route('/travel-lists', methods=['POST'])
@jwt_required()
def create_travel_list():
    data = request.json
    try:
        list_id = travel_list_controller.create_travel_list(
            data['user_id'],
            data['name'],
            data['description']
        )
        return jsonify({"message": "Travel list created successfully", "list_id": list_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener una lista de viaje existente
@travel_list_routes.route('/travel-lists/<int:list_id>', methods=['GET'])
@jwt_required()
def get_travel_list(list_id):
    travel_list = travel_list_controller.get_travel_list(list_id)
    if travel_list:
        return jsonify(travel_list.to_dict()), 200
    else:
        return jsonify({"error": "Travel list not found"}), 404
    
# Actualizar una lista de viaje existente
@travel_list_routes.route('/travel-lists/<int:list_id>', methods=['PUT'])
@jwt_required()
def update_travel_list(list_id):
    current_user_id = get_jwt_identity()
    data = request.json
    try:
        # Verificar si la lista de viaje pertenece al usuario actual
        travel_list = travel_list_controller.get_travel_list(list_id)
        if not travel_list or travel_list.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        updated_list_id = travel_list_controller.update_travel_list(
            list_id,
            data['name'],
            data['description']
        )
        if updated_list_id:
            return jsonify({"message": "Travel list updated successfully", "list_id": updated_list_id}), 200
        else:
            return jsonify({"error": "Travel list not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar una lista de viaje existente
@travel_list_routes.route('/travel-lists/<int:list_id>', methods=['DELETE'])
@jwt_required()
def delete_travel_list(list_id):
    current_user_id = get_jwt_identity()
    try:
        # Verificar si la lista de viaje pertenece al usuario actual
        travel_list = travel_list_controller.get_travel_list(list_id)
        if not travel_list or travel_list.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        deleted_list_id = travel_list_controller.delete_travel_list(list_id)
        if deleted_list_id:
            return jsonify({"message": "Travel list deleted successfully", "list_id": deleted_list_id}), 200
        else:
            return jsonify({"error": "Travel list not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Agregar un lugar a una lista de viaje
@travel_list_routes.route('/travel-lists/<int:list_id>/places', methods=['POST'])
@jwt_required()
def add_place_to_list(list_id):
    current_user_id = get_jwt_identity()
    data = request.json
    try:
        # Verificar si la lista de viaje pertenece al usuario actual
        travel_list = travel_list_controller.get_travel_list(list_id)
        if not travel_list or travel_list.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        new_entry_id = travel_list_controller.add_place_to_list(list_id, data['place_id'])
        if new_entry_id:
            return jsonify({"message": "Place added to travel list successfully", "entry_id": new_entry_id}), 201
        else:
            return jsonify({"error": "Failed to add place to travel list"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un lugar de una lista de viaje
@travel_list_routes.route('/travel-lists/<int:list_id>/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
def remove_place_from_list(list_id, place_id):
    current_user_id = get_jwt_identity()
    try:
        # Verificar si la lista de viaje pertenece al usuario actual
        travel_list = travel_list_controller.get_travel_list(list_id)
        if not travel_list or travel_list.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        deleted_entry_id = travel_list_controller.remove_place_from_list(list_id, place_id)
        if deleted_entry_id:
            return jsonify({"message": "Place removed from travel list successfully", "entry_id": deleted_entry_id}), 200
        else:
            return jsonify({"error": "Place not found in travel list"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener los lugares de una lista de viaje
@travel_list_routes.route('/travel-lists/<int:list_id>/places', methods=['GET'])
@jwt_required()
def get_places_in_list(list_id):
    current_user_id = get_jwt_identity()
    try:
        # Verificar si la lista de viaje pertenece al usuario actual
        travel_list = travel_list_controller.get_travel_list(list_id)
        if not travel_list or travel_list.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        places = travel_list_controller.get_places_in_list(list_id)
        return jsonify([place.to_dict() for place in places]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
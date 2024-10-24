from flask import Blueprint, request, jsonify
from controllers import place_controller
from flask_jwt_extended import jwt_required

place_routes = Blueprint('place_routes', __name__)

# Crear un nuevo lugar
@place_routes.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    data = request.json
    try:
        place_id = place_controller.create_place(
            data['name'],
            data['description'],
            data['city'],
            data['country']
        )
        return jsonify({"message": "Place created successfully", "place_id": place_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un lugar por ID
@place_routes.route('/places/<int:place_id>', methods=['GET'])
@jwt_required()
def get_place(place_id):
    place = place_controller.get_place(place_id)
    if place:
        return jsonify(place.to_dict() if hasattr(place, 'to_dict') else place), 200
    else:
        return jsonify({"error": "Place not found"}), 404
    
# Actualizar un lugar existente
@place_routes.route('/places/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    data = request.json
    try:
        updated_place_id = place_controller.update_place(
            place_id,
            data['name'],
            data['description'],
            data['city'],
            data['country']
        )
        if updated_place_id:
            return jsonify({"message": "Place updated successfully", "place_id": updated_place_id}), 200
        else:
            return jsonify({"error": "Place not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un lugar existente
@place_routes.route('/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    try:
        deleted_place_id = place_controller.delete_place(place_id)
        if deleted_place_id:
            return jsonify({"message": "Place deleted successfully", "place_id": deleted_place_id}), 200
        else:
            return jsonify({"error": "Place not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
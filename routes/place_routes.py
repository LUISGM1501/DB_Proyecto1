from flask import Blueprint, request, jsonify
from controllers import place_controller

place_routes = Blueprint('place_routes', __name__)

# Crear un nuevo lugar
@place_routes.route('/places', methods=['POST'])
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
def get_place(place_id):
    place = place_controller.get_place(place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        return jsonify({"error": "Place not found"}), 404
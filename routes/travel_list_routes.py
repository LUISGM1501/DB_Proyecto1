from flask import Blueprint, request, jsonify
from controllers import travel_list_controller

travel_list_routes = Blueprint('travel_list_routes', __name__)

@travel_list_routes.route('/travel-lists', methods=['POST'])
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

@travel_list_routes.route('/travel-lists/<int:list_id>', methods=['GET'])
def get_travel_list(list_id):
    travel_list = travel_list_controller.get_travel_list(list_id)
    if travel_list:
        return jsonify(travel_list.to_dict()), 200
    else:
        return jsonify({"error": "Travel list not found"}), 404
# routes/mongo_routes.py
from flask import Blueprint, request, jsonify
from controllers.mongo_controller import MongoController
from flask_jwt_extended import jwt_required, get_jwt_identity

mongo_routes = Blueprint('mongo_routes', __name__)
mongo_controller = MongoController()

@mongo_routes.route('/travels', methods=['POST'])
@jwt_required()
def create_travel():
    current_user_id = get_jwt_identity()
    travel_data = request.json
    
    result = mongo_controller.create_travel_record(current_user_id, travel_data)
    
    if result['status'] == 'success':
        return jsonify(result), 201
    return jsonify(result), 400

@mongo_routes.route('/places/<int:place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    current_user_id = get_jwt_identity()
    review_data = request.json
    
    result = mongo_controller.create_detailed_review(current_user_id, place_id, review_data)
    
    if result['status'] == 'success':
        return jsonify(result), 201
    return jsonify(result), 400

@mongo_routes.route('/users/activity', methods=['GET'])
@jwt_required()
def get_user_activity():
    current_user_id = get_jwt_identity()
    
    result = mongo_controller.get_user_activity_summary(current_user_id)
    
    if result['status'] == 'success':
        return jsonify(result), 200
    return jsonify(result), 400

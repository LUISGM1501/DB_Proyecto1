from flask import Blueprint, request, jsonify
from controllers import like_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

like_routes = Blueprint('like_routes', __name__)

@like_routes.route('/likes', methods=['POST'])
@jwt_required()
def add_like():
    data = request.json
    try:
        success = like_controller.add_like(
            data['user_id'],
            data.get('post_id'),
            data.get('place_id')
        )
        if success:
            return jsonify({"message": "Like added successfully"}), 201
        else:
            return jsonify({"message": "Like already exists"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@like_routes.route('/likes/count', methods=['GET'])
@jwt_required()
def get_like_count():
    post_id = request.args.get('post_id')
    place_id = request.args.get('place_id')
    count = like_controller.get_like_count(post_id, place_id)
    return jsonify({"count": count}), 200
# routes/follow_routes.py
from flask import Blueprint, request, jsonify
from controllers import follow_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

follow_routes = Blueprint('follow_routes', __name__)

# Seguir a un usuario
@follow_routes.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    try:
        new_follow_id = follow_controller.follow_user(current_user_id, user_id)
        if new_follow_id:
            return jsonify({"message": "User followed successfully", "follow_id": new_follow_id}), 201
        else:
            return jsonify({"error": "Failed to follow user"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Dejar de seguir a un usuario
@follow_routes.route('/unfollow/<int:user_id>', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    try:
        deleted_follow_id = follow_controller.unfollow_user(current_user_id, user_id)
        if deleted_follow_id:
            return jsonify({"message": "User unfollowed successfully", "follow_id": deleted_follow_id}), 200
        else:
            return jsonify({"error": "User was not being followed"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener los usuarios seguidos por un usuario
@follow_routes.route('/following', methods=['GET'])
@jwt_required()
def get_followed_users():
    current_user_id = get_jwt_identity()
    try:
        followed_users = follow_controller.get_followed_users(current_user_id)
        return jsonify([user.to_dict() for user in followed_users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener los seguidores de un usuario
@follow_routes.route('/followers', methods=['GET'])
@jwt_required()
def get_followers():
    current_user_id = get_jwt_identity()
    try:
        followers = follow_controller.get_followers(current_user_id)
        return jsonify([user.to_dict() for user in followers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener el feed de un usuario
@follow_routes.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    current_user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    try:
        feed_posts = follow_controller.get_feed(current_user_id, page, page_size)
        return jsonify(feed_posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
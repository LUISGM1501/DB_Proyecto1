from flask import Blueprint, request, jsonify
from controllers import comment_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_routes = Blueprint('comment_routes', __name__)

# Crear un nuevo comentario
@comment_routes.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.json
    try:
        comment_id = comment_controller.create_comment(
            data['user_id'],
            data['content'],
            data.get('post_id'),
            data.get('place_id')
        )
        return jsonify({"message": "Comment created successfully", "comment_id": comment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener comentarios de un post o lugar
@comment_routes.route('/comments', methods=['GET'])
@jwt_required()
def get_comments():
    post_id = request.args.get('post_id')
    place_id = request.args.get('place_id')
    comments = comment_controller.get_comments(post_id, place_id)

    return jsonify([comment.to_dict() if hasattr(comment, 'to_dict') else comment for comment in comments]), 200
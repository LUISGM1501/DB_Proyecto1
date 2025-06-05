# routes/post_routes.py
from flask import Blueprint, request, jsonify
from controllers import post_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

post_routes = Blueprint('post_routes', __name__)

# Crear un nuevo post
@post_routes.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.json
    try:
        post_id = post_controller.create_post(
            data['user_id'],
            data['content']
        )
        return jsonify({"message": "Post created successfully", "post_id": post_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un post por ID
@post_routes.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = post_controller.get_post(post_id)
    if post:
        return jsonify(post.to_dict() if hasattr(post, 'to_dict') else post), 200
    else:
        return jsonify({"error": "Post not found"}), 404
    
# Obtener publicaciones paginadas
@post_routes.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    posts, total_count = post_controller.get_posts_paginated(page, page_size)
    return jsonify({
        "posts": [post.to_dict() if hasattr(post, 'to_dict') else post for post in posts],
        "total_count": total_count,
        "page": page,
        "page_size": page_size
    }), 200

# Actualizar un post existente
@post_routes.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    data = request.json
    try:
        # Verificar si el post pertenece al usuario actual
        post = post_controller.get_post(post_id)
        if not post or post.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        updated_post_id = post_controller.update_post(post_id, data['content'])
        if updated_post_id:
            return jsonify({"message": "Post updated successfully", "post_id": updated_post_id}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un post existente
@post_routes.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    try:
        # Verificar si el post pertenece al usuario actual
        post = post_controller.get_post(post_id)
        if not post or post.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        deleted_post_id = post_controller.delete_post(post_id)
        if deleted_post_id:
            return jsonify({"message": "Post deleted successfully", "post_id": deleted_post_id}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
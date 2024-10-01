from flask import Blueprint, request, jsonify
from controllers import post_controller

post_routes = Blueprint('post_routes', __name__)

# Crear un nuevo post
@post_routes.route('/posts', methods=['POST'])
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
def get_post(post_id):
    post = post_controller.get_post(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({"error": "Post not found"}), 404
    
# Obtener publicaciones paginadas
@post_routes.route('/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    posts, total_count = post_controller.get_posts_paginated(page, page_size)
    return jsonify({
        "posts": [post.to_dict() for post in posts],
        "total_count": total_count,
        "page": page,
        "page_size": page_size
    }), 200
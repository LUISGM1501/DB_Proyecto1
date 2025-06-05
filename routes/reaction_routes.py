# routes/reaction_routes.py
from flask import Blueprint, request, jsonify
from controllers import reaction_controller
from flask_jwt_extended import jwt_required, get_jwt_identity

reaction_routes = Blueprint('reaction_routes', __name__)

@reaction_routes.route('/reactions', methods=['POST'])
@jwt_required()
def add_or_update_reaction():
    data = request.json
    try:
        success = reaction_controller.add_or_update_reaction(
            data['user_id'],
            data['post_id'],
            data['reaction_type']
        )
        if success:
            return jsonify({"message": "Reaction added/updated successfully"}), 201
        else:
            return jsonify({"message": "Failed to add/update reaction"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@reaction_routes.route('/reactions/count/<int:post_id>', methods=['GET'])
def get_reaction_counts(post_id):
    counts = reaction_controller.get_reaction_counts(post_id)
    return jsonify({"counts": dict(counts)}), 200
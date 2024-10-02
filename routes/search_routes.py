from flask import Blueprint, request, jsonify
from controllers import search_controller
from flask_jwt_extended import jwt_required

search_routes = Blueprint('search_routes', __name__)

@search_routes.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('q', '')
    results = search_controller.search_content(query)
    return jsonify(results), 200
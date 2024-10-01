from flask import Blueprint, request, jsonify
from controllers import search_controller

search_routes = Blueprint('search_routes', __name__)

@search_routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = search_controller.search_content(query)
    return jsonify(results), 200
# middleware/error_handler.py
from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def handle_400_error(e):
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    @app.errorhandler(401)
    def handle_401_error(e):
        return jsonify({"error": "Unauthorized", "message": str(e)}), 401

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({"error": "Not Found", "message": str(e)}), 404

    @app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import notification_controller

notification_routes = Blueprint('notification_routes', __name__)

# Obtener las notificaciones de un usuario
@notification_routes.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    notifications = notification_controller.get_user_notifications(current_user_id, limit, offset)
    return jsonify(notifications), 200

# Marcar una notificacion como leida
@notification_routes.route('/notifications/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    success = notification_controller.mark_notification_as_read(notification_id)
    if success:
        return jsonify({"message": "Notification marked as read"}), 200
    else:
        return jsonify({"error": "Failed to mark notification as read"}), 400


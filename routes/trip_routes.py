# routes/trip_routes.py
from flask import Blueprint, request, jsonify
from controllers import trip_controller
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

trip_routes = Blueprint('trip_routes', __name__)

# Crear un nuevo viaje
@trip_routes.route('/trips', methods=['POST'])
@jwt_required()
def create_trip():
    current_user_id = get_jwt_identity()
    data = request.json
    
    # Validaciones básicas
    required_fields = ['title', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        trip_id = trip_controller.create_trip(
            user_id=current_user_id,
            title=data['title'],
            description=data.get('description', ''),
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data.get('status', 'planned'),
            budget=data.get('budget')
        )
        return jsonify({"message": "Trip created successfully", "trip_id": trip_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un viaje por ID
@trip_routes.route('/trips/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    try:
        trip = trip_controller.get_trip(trip_id)
        if trip:
            # Verificar que el usuario actual puede ver este viaje
            current_user_id = get_jwt_identity()
            if trip.user_id != current_user_id:
                return jsonify({"error": "Unauthorized to view this trip"}), 403
            
            return jsonify(trip.to_dict()), 200
        else:
            return jsonify({"error": "Trip not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener viajes del usuario actual
@trip_routes.route('/trips', methods=['GET'])
@jwt_required()
def get_user_trips():
    current_user_id = get_jwt_identity()
    
    # Parámetros de consulta opcionales
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    try:
        trips, total_count = trip_controller.get_user_trips(
            current_user_id, status, page, page_size
        )
        return jsonify({
            "trips": [trip.to_dict() for trip in trips],
            "total_count": total_count,
            "page": page,
            "page_size": page_size
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Actualizar un viaje
@trip_routes.route('/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    current_user_id = get_jwt_identity()
    data = request.json
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        updated_trip_id = trip_controller.update_trip(
            trip_id=trip_id,
            title=data.get('title', trip.title),
            description=data.get('description', trip.description),
            start_date=data.get('start_date', trip.start_date),
            end_date=data.get('end_date', trip.end_date),
            status=data.get('status', trip.status),
            budget=data.get('budget', trip.budget)
        )
        
        if updated_trip_id:
            return jsonify({"message": "Trip updated successfully", "trip_id": updated_trip_id}), 200
        else:
            return jsonify({"error": "Failed to update trip"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un viaje
@trip_routes.route('/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    current_user_id = get_jwt_identity()
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        deleted_trip_id = trip_controller.delete_trip(trip_id)
        if deleted_trip_id:
            return jsonify({"message": "Trip deleted successfully", "trip_id": deleted_trip_id}), 200
        else:
            return jsonify({"error": "Failed to delete trip"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Agregar un lugar a un viaje
@trip_routes.route('/trips/<int:trip_id>/places', methods=['POST'])
@jwt_required()
def add_place_to_trip(trip_id):
    current_user_id = get_jwt_identity()
    data = request.json
    
    if 'place_id' not in data:
        return jsonify({"error": "Missing required field: place_id"}), 400
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        entry_id = trip_controller.add_place_to_trip(
            trip_id=trip_id,
            place_id=data['place_id'],
            visit_date=data.get('visit_date'),
            visit_order=data.get('visit_order'),
            notes=data.get('notes'),
            rating=data.get('rating')
        )
        
        if entry_id:
            return jsonify({"message": "Place added to trip successfully", "entry_id": entry_id}), 201
        else:
            return jsonify({"error": "Failed to add place to trip"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un lugar de un viaje
@trip_routes.route('/trips/<int:trip_id>/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
def remove_place_from_trip(trip_id, place_id):
    current_user_id = get_jwt_identity()
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        deleted_entry_id = trip_controller.remove_place_from_trip(trip_id, place_id)
        if deleted_entry_id:
            return jsonify({"message": "Place removed from trip successfully", "entry_id": deleted_entry_id}), 200
        else:
            return jsonify({"error": "Place not found in trip"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener los lugares de un viaje
@trip_routes.route('/trips/<int:trip_id>/places', methods=['GET'])
@jwt_required()
def get_trip_places(trip_id):
    current_user_id = get_jwt_identity()
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        places = trip_controller.get_trip_places(trip_id)
        return jsonify({"places": places}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener estadísticas de un viaje
@trip_routes.route('/trips/<int:trip_id>/statistics', methods=['GET'])
@jwt_required()
def get_trip_statistics(trip_id):
    current_user_id = get_jwt_identity()
    
    try:
        # Verificar que el viaje pertenece al usuario actual
        trip = trip_controller.get_trip(trip_id)
        if not trip or trip.user_id != current_user_id:
            return jsonify({"error": "Unauthorized or trip not found"}), 403
        
        statistics = trip_controller.get_trip_statistics(trip_id)
        if statistics:
            return jsonify(statistics), 200
        else:
            return jsonify({"error": "Failed to get trip statistics"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Buscar viajes (funcionalidad avanzada)
@trip_routes.route('/trips/search', methods=['GET'])
@jwt_required()
def search_trips():
    current_user_id = get_jwt_identity()
    
    # Parámetros de búsqueda
    status = request.args.get('status')
    start_date_from = request.args.get('start_date_from')
    start_date_to = request.args.get('start_date_to')
    title_search = request.args.get('title')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    try:
        trips, total_count = trip_controller.search_trips(
            user_id=current_user_id,
            status=status,
            start_date_from=start_date_from,
            start_date_to=start_date_to,
            title_search=title_search,
            page=page,
            page_size=page_size
        )
        
        return jsonify({
            "trips": [trip.to_dict() for trip in trips],
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "search_criteria": {
                "status": status,
                "start_date_from": start_date_from,
                "start_date_to": start_date_to,
                "title": title_search
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
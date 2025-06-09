# controllers/trip_controller.py
from models.trip import Trip, TripPlace
from config.database import get_postgres_connection
from datetime import date

# Crear un nuevo viaje
def create_trip(user_id, title, description, start_date, end_date, status='planned', budget=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para crear un nuevo viaje
            cur.execute(
                "SELECT create_trip(%s, %s, %s, %s, %s, %s, %s)",
                (user_id, title, description, start_date, end_date, status, budget)
            )
            # Obtiene el ID del viaje recién creado
            trip_id = cur.fetchone()[0]
        conn.commit()  # Confirma la transacción
        return trip_id  # Devuelve el ID del viaje
    except Exception as e:
        conn.rollback()  # Revierte la transacción en caso de error
        raise e  # Lanza la excepción
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Obtener un viaje por ID
def get_trip(trip_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para obtener un viaje por su ID
            cur.execute("SELECT * FROM get_trip_by_id(%s)", (trip_id,))
            trip_data = cur.fetchone()  # Obtiene los datos del viaje
            if trip_data:
                # Crea y devuelve un objeto Trip con los datos obtenidos
                return Trip(
                    user_id=trip_data[1],
                    title=trip_data[2],
                    description=trip_data[3],
                    start_date=trip_data[4],
                    end_date=trip_data[5],
                    status=trip_data[6],
                    budget=trip_data[7],
                    id=trip_data[0]
                )
            return None  # Devuelve None si no se encuentra el viaje
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Obtener viajes de un usuario con paginación
def get_user_trips(user_id, status=None, page=1, page_size=10):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para obtener viajes de un usuario con paginación
            cur.execute("SELECT * FROM get_user_trips(%s, %s, %s, %s)", 
                       (user_id, status, page, page_size))
            trips_data = cur.fetchall()  # Obtiene todos los datos de los viajes
            if trips_data:
                total_count = trips_data[0][-1]  # último campo es total_count
                trips = []
                for row in trips_data:
                    # Crea un objeto Trip para cada fila de datos y lo agrega a la lista
                    trip = Trip(
                        user_id=row[1],
                        title=row[2],
                        description=row[3],
                        start_date=row[4],
                        end_date=row[5],
                        status=row[6],
                        budget=row[7],
                        id=row[0]
                    )
                    trips.append(trip)
                return trips, total_count  # Devuelve la lista de viajes y el total
            return [], 0  # Devuelve una lista vacía y 0 si no hay viajes
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Actualizar un viaje existente
def update_trip(trip_id, title, description, start_date, end_date, status, budget):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para actualizar un viaje existente
            cur.execute(
                "SELECT update_trip(%s, %s, %s, %s, %s, %s, %s)",
                (trip_id, title, description, start_date, end_date, status, budget)
            )
            updated_trip_id = cur.fetchone()  # Obtiene el ID del viaje actualizado
            if updated_trip_id:
                conn.commit()  # Confirma la transacción
                return updated_trip_id[0]  # Devuelve el ID del viaje actualizado
            return None  # Devuelve None si no se actualiza el viaje
    except Exception as e:
        conn.rollback()  # Revierte la transacción en caso de error
        raise e  # Lanza la excepción
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Eliminar un viaje existente
def delete_trip(trip_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para eliminar un viaje existente
            cur.execute("SELECT delete_trip(%s)", (trip_id,))
            deleted_trip_id = cur.fetchone()  # Obtiene el ID del viaje eliminado
            if deleted_trip_id:
                conn.commit()  # Confirma la transacción
                return deleted_trip_id[0]  # Devuelve el ID del viaje eliminado
            return None  # Devuelve None si no se elimina el viaje
    except Exception as e:
        conn.rollback()  # Revierte la transacción en caso de error
        raise e  # Lanza la excepción
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Agregar un lugar a un viaje
def add_place_to_trip(trip_id, place_id, visit_date=None, visit_order=None, notes=None, rating=None):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para agregar un lugar a un viaje
            cur.execute(
                "SELECT add_place_to_trip(%s, %s, %s, %s, %s, %s)",
                (trip_id, place_id, visit_date, visit_order, notes, rating)
            )
            new_entry_id = cur.fetchone()  # Obtiene el ID de la nueva entrada
            conn.commit()  # Confirma la transacción
            return new_entry_id[0] if new_entry_id else None  # Devuelve el ID de la nueva entrada o None
    except Exception as e:
        conn.rollback()  # Revierte la transacción en caso de error
        raise e  # Lanza la excepción
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Eliminar un lugar de un viaje
def remove_place_from_trip(trip_id, place_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para eliminar un lugar de un viaje
            cur.execute("SELECT remove_place_from_trip(%s, %s)", (trip_id, place_id))
            deleted_entry_id = cur.fetchone()  # Obtiene el ID de la entrada eliminada
            conn.commit()  # Confirma la transacción
            return deleted_entry_id[0] if deleted_entry_id else None  # Devuelve el ID de la entrada eliminada o None
    except Exception as e:
        conn.rollback()  # Revierte la transacción en caso de error
        raise e  # Lanza la excepción
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Obtener los lugares de un viaje
def get_trip_places(trip_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para obtener los lugares de un viaje
            cur.execute("SELECT * FROM get_trip_places(%s)", (trip_id,))
            places_data = cur.fetchall()  # Obtiene todos los datos de los lugares
            places = []
            for row in places_data:
                # Crea un diccionario con la información del lugar y lo agrega a la lista
                place_info = {
                    "place_id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "city": row[3],
                    "country": row[4],
                    "visit_date": row[5].isoformat() if row[5] else None,
                    "visit_order": row[6],
                    "notes": row[7],
                    "rating": row[8]
                }
                places.append(place_info)
            return places  # Devuelve la lista de lugares
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Obtener estadísticas de un viaje
def get_trip_statistics(trip_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Ejecuta la función SQL para obtener estadísticas de un viaje
            cur.execute("SELECT * FROM get_trip_statistics(%s)", (trip_id,))
            stats_data = cur.fetchone()  # Obtiene los datos de las estadísticas
            if stats_data:
                # Crea y devuelve un diccionario con las estadísticas del viaje
                return {
                    "total_places": stats_data[0],
                    "total_expenses": float(stats_data[1]) if stats_data[1] else 0,
                    "avg_place_rating": float(stats_data[2]) if stats_data[2] else None,
                    "trip_duration_days": stats_data[3]
                }
            return None  # Devuelve None si no se encuentran estadísticas
    finally:
        conn.close()  # Cierra la conexión a la base de datos

# Buscar viajes por criterios
def search_trips(user_id=None, status=None, start_date_from=None, start_date_to=None, 
                title_search=None, page=1, page_size=10):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # Construir consulta dinámica
            conditions = []  # Lista para almacenar las condiciones de búsqueda
            params = []  # Lista para almacenar los parámetros de búsqueda
            
            if user_id:
                conditions.append("t.user_id = %s")  # Agrega condición para el ID de usuario
                params.append(user_id)  # Agrega el ID de usuario a los parámetros
            
            if status:
                conditions.append("t.status = %s")  # Agrega condición para el estado
                params.append(status)  # Agrega el estado a los parámetros
            
            if start_date_from:
                conditions.append("t.start_date >= %s")  # Agrega condición para la fecha de inicio
                params.append(start_date_from)  # Agrega la fecha de inicio a los parámetros
            
            if start_date_to:
                conditions.append("t.start_date <= %s")  # Agrega condición para la fecha de fin
                params.append(start_date_to)  # Agrega la fecha de fin a los parámetros
            
            if title_search:
                # Agrega condición para la búsqueda en el título usando un vector de búsqueda
                conditions.append("t.search_vector @@ plainto_tsquery('english', %s)")
                params.append(title_search)  # Agrega el término de búsqueda al título
            
            # Construye la cláusula WHERE de la consulta
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            # Agregar paginación
            params.extend([page_size, (page - 1) * page_size])  # Agrega los parámetros de paginación
            
            # Construye la consulta SQL completa
            query = f"""
                SELECT t.*, COUNT(*) OVER() as total_count
                FROM trips t
                WHERE {where_clause}
                ORDER BY t.start_date DESC
                LIMIT %s OFFSET %s
            """
            
            cur.execute(query, params)  # Ejecuta la consulta con los parámetros
            trips_data = cur.fetchall()  # Obtiene todos los datos de los viajes
            
            if trips_data:
                total_count = trips_data[0][-1]  # último campo
                trips = []
                for row in trips_data[:-1]:  # excluir total_count
                    # Crea un objeto Trip para cada fila de datos y lo agrega a la lista
                    trip = Trip(
                        user_id=row[1],
                        title=row[2],
                        description=row[3],
                        start_date=row[4],
                        end_date=row[5],
                        status=row[6],
                        budget=row[7],
                        id=row[0]
                    )
                    trips.append(trip)
                return trips, total_count  # Devuelve la lista de viajes y el total
            return [], 0  # Devuelve una lista vacía y 0 si no hay viajes
    finally:
        conn.close()  # Cierra la conexión a la base de datos
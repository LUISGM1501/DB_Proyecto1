from models.travel_list import TravelList
from config.database import get_postgres_connection
from models.place import Place

# Crear una nueva lista de viaje
def create_travel_list(user_id, name, description):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_travel_list(%s, %s, %s)",
                (user_id, name, description)
            )
            list_id = cur.fetchone()[0]
        conn.commit()
        return list_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener una lista de viaje por ID
def get_travel_list(list_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_travel_list_by_id(%s)", (list_id,))
            list_data = cur.fetchone()
            if list_data:
                return TravelList(*list_data)
            return None
    finally:
        conn.close()

# Actualizar una lista de viaje existente
def update_travel_list(list_id, name, description):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT update_travel_list(%s, %s, %s)", (list_id, name, description))
            updated_list_id = cur.fetchone()
            conn.commit()
            return updated_list_id[0] if updated_list_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Eliminar una lista de viaje existente
def delete_travel_list(list_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT delete_travel_list(%s)", (list_id,))
            deleted_list_id = cur.fetchone()
            conn.commit()
            return deleted_list_id[0] if deleted_list_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Agregar un lugar a una lista de viaje
def add_place_to_list(list_id, place_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT add_place_to_list(%s, %s)", (list_id, place_id))
            new_entry_id = cur.fetchone()
            conn.commit()
            return new_entry_id[0] if new_entry_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Eliminar un lugar de una lista de viaje
def remove_place_from_list(list_id, place_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT remove_place_from_list(%s, %s)", (list_id, place_id))
            deleted_entry_id = cur.fetchone()
            conn.commit()
            return deleted_entry_id[0] if deleted_entry_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener los lugares de una lista de viaje
def get_places_in_list(list_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_places_in_list(%s)", (list_id,))
            places_data = cur.fetchall()
            return [Place(*place_data) for place_data in places_data]
    finally:
        conn.close()
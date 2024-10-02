from models.place import Place
from config.database import get_postgres_connection

# Crear un nuevo lugar
def create_place(name, description, city, country):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT create_place(%s, %s, %s, %s)",
                (name, description, city, country)
            )
            place_id = cur.fetchone()[0]
        conn.commit()
        return place_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Obtener un lugar por ID
def get_place(place_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_place_by_id(%s)", (place_id,))
            place_data = cur.fetchone()
            if place_data:
                return Place(*place_data)
            return None
    finally:
        conn.close()

# Actualizar un lugar existente
def update_place(place_id, name, description, city, country):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT update_place(%s, %s, %s, %s, %s)",
                (place_id, name, description, city, country)
            )
            updated_place_id = cur.fetchone()
            conn.commit()
            return updated_place_id[0] if updated_place_id else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Eliminar un lugar existente
def delete_place(place_id):
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT delete_place(%s)", (place_id,))
            deleted_place_id = cur.fetchone()
            if deleted_place_id:
                conn.commit()
                return deleted_place_id[0]
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
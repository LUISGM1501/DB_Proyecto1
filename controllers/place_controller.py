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